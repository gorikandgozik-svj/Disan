"""Minimal stdlib JSON-RPC 2.0 MCP stdio implementation.

Communicates using newline-separated JSON messages. Never emits debug logs to
stdout. Tool failures are reported as tool errors, not JSON-RPC transport errors.
"""
import json
import sys
from core import TOOLS, dispatch

VERSION = '2025-03-26'
SERVER_VERSION = '1.1.0'


def _error(ident, code, message):
    return {'jsonrpc': '2.0', 'id': ident, 'error': {'code': code, 'message': message}}


def respond(request):
    if not isinstance(request, dict) or request.get('jsonrpc') != '2.0':
        return _error(request.get('id') if isinstance(request, dict) else None, -32600, 'Invalid Request')
    method = request.get('method')
    if not isinstance(method, str):
        return _error(request.get('id'), -32600, 'Invalid Request')
    if 'id' not in request:
        return None  # JSON-RPC notifications never get replies
    ident = request['id']
    if isinstance(ident, bool) or not isinstance(ident, (str, int)):
        return _error(None, -32600, 'Invalid id')
    params = request.get('params', {})
    if not isinstance(params, dict):
        return _error(ident, -32602, 'params must be an object')
    if method == 'initialize':
        result = {'protocolVersion': VERSION, 'capabilities': {'tools': {'listChanged': False}},
                  'serverInfo': {'name': 'vibe-visual-forge-local', 'version': SERVER_VERSION}}
    elif method == 'ping':
        result = {}
    elif method == 'tools/list':
        result = {'tools': TOOLS}
    elif method == 'tools/call':
        tool_name = params.get('name', '')
        args = params.get('arguments', {})
        if not isinstance(args, dict):
            return _error(ident, -32602, 'Tool arguments must be an object')
        try:
            result_data = dispatch(tool_name, args)
            result = {'content': [{'type': 'text', 'text': json.dumps(result_data, ensure_ascii=False, indent=2)}],
                      'isError': False}
        except Exception as exc:
            print(f'Tool error [{tool_name}]: {type(exc).__name__}: {exc}', file=sys.stderr)
            result = {'content': [{'type': 'text', 'text': f'{type(exc).__name__}: {exc}'}],
                      'isError': True}
    else:
        return _error(ident, -32601, 'Method not found')
    return {'jsonrpc': '2.0', 'id': ident, 'result': result}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            response = _error(None, -32700, 'Parse error')
        else:
            try:
                response = respond(request)
            except Exception as exc:
                print(f'Unexpected protocol exception: {exc}', file=sys.stderr)
                response = _error(request.get('id') if isinstance(request, dict) else None, -32603, 'Internal error')
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False, separators=(',', ':')) + '\n')
            sys.stdout.flush()


if __name__ == '__main__':
    main()
