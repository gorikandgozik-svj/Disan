"""Optional local, finite-step job executor.

This is NOT an AI background process. It executes only explicit, allow-listed
JSON tasks in the user's project workspace. There is no network or arbitrary
shell execution, no auto-installation, and no retry loop on failures.
"""
from __future__ import annotations
import argparse
import json
import os
import signal
import sys
import time
import uuid
from pathlib import Path
from core import dispatch, root_dir, TOOLS

ALLOWED = frozenset(tool['name'] for tool in TOOLS)
MAX_TASK_BYTES = 64 * 1024
STALE_AFTER_SECONDS = 1800


def _write_atomic(path: Path, record: dict):
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        temp.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def process_once(max_jobs=50):
    """Consume at most max_jobs. Failed and stale jobs go to failed/, never retried."""
    if isinstance(max_jobs, bool) or not 1 <= int(max_jobs) <= 500:
        raise ValueError('max_jobs must be 1..500')
    q = root_dir() / 'queue'
    inbox, done, failed = (q / k for k in ('inbox', 'done', 'failed'))
    for directory in (inbox, done, failed):
        directory.mkdir(parents=True, exist_ok=True)
    reports = []

    # On restart, report interrupted tasks instead of silently orphaning them.
    for claimed in sorted(inbox.glob('*.working')):
        if time.time() - claimed.stat().st_mtime < STALE_AFTER_SECONDS:
            continue
        record = {'status': 'failed', 'reason': 'Job interrupted by stopped worker; no auto-retry'}
        _write_atomic(failed / (claimed.name + '.result.json'), record)
        claimed.unlink(missing_ok=True)
        reports.append({'job': claimed.name, 'status': 'failed'})

    for file in sorted(inbox.glob('*.json'))[:int(max_jobs)]:
        claimed = inbox / (file.name + '.' + uuid.uuid4().hex + '.working')
        try:
            # Files in inbox must be regular files, not symlinks.
            if file.is_symlink():
                file.unlink()
                reports.append({'job': file.name, 'status': 'rejected-symlink'})
                continue
            file.rename(claimed)
        except FileNotFoundError:
            continue  # another worker claimed it
        try:
            if not claimed.is_file() or claimed.stat().st_size > MAX_TASK_BYTES:
                raise ValueError('Task is not a regular JSON file or exceeds 64 KiB')
            doc = json.loads(claimed.read_text(encoding='utf-8'))
            if not isinstance(doc, dict):
                raise ValueError('Task must be a JSON object')
            tool = doc.get('tool')
            arguments = doc.get('arguments', {})
            if tool not in ALLOWED or not isinstance(arguments, dict):
                raise ValueError('Tool is not allowed or arguments must be an object')
            result = dispatch(tool, arguments)
            record = {'status': 'completed', 'tool': tool, 'result': result}
            directory = done
        except Exception as e:
            record = {'status': 'failed', 'error': f'{type(e).__name__}: {e}'}
            directory = failed
        _write_atomic(directory / (file.stem + '.result.json'), record)
        claimed.unlink(missing_ok=True)
        reports.append({'job': file.stem, 'status': record['status']})
    return reports


def main():
    parser = argparse.ArgumentParser(description='Local visual task queue (requires explicit launch)')
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--interval', type=float, default=3.0)
    args = parser.parse_args()
    running = True

    def stop(_signum, _frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, stop)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, stop)
    if args.once:
        print(json.dumps(process_once(), ensure_ascii=False))
        return
    print(f'Local task queue running in {root_dir()}; Ctrl+C to stop.', flush=True)
    while running:
        try:
            for status in process_once():
                print(json.dumps(status, ensure_ascii=False), flush=True)
        except Exception as error:
            print(f'Queue error: {error}', file=sys.stderr, flush=True)
        time.sleep(max(1, min(args.interval, 120)))


if __name__ == '__main__':
    main()
