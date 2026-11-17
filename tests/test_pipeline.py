"""Regression, security, integration and actual GLB validation tests."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SERVER = Path(__file__).resolve().parents[1] / 'server'
sys.path.insert(0, str(SERVER))
from core import (
    slug, TOOLS, dispatch, create_ui_prototype, create_city_blockout,
    compare_screenshots, audit_ui, STYLES,
)
from procedural_assets import audit_3d, create_vehicle_blockout, create_winter_environment
from watch import process_once, MAX_TASK_BYTES


class Fixture(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix='vfqa-')
        self.old = os.environ.get('VF_WORKSPACE_DIR')
        os.environ['VF_WORKSPACE_DIR'] = self.workspace.name

    def tearDown(self):
        if self.old is None:
            os.environ.pop('VF_WORKSPACE_DIR', None)
        else:
            os.environ['VF_WORKSPACE_DIR'] = self.old
        self.workspace.cleanup()


class SafetyTests(Fixture):
    def test_non_ascii_names_do_not_collide(self):
        self.assertNotEqual(slug('Город'), slug('Самолёт'))
        self.assertNotEqual(slug('🤖'), slug('✈️'))

    def test_slug_is_safe_and_stable(self):
        name = '../../tmp/../../test'
        self.assertEqual(slug(name), slug(name))
        self.assertNotIn('/', slug(name))
        self.assertNotIn('..', slug(name))

    def test_empty_and_very_long_project_names_rejected(self):
        for value in ['', '   ', 'A' * 500, None]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    slug(value)

    def test_unknown_tool_rejected(self):
        for payload in ['os.system', 'bash', '__import__']:
            with self.assertRaises(ValueError):
                dispatch(payload, {})

    def test_bad_style_rejected(self):
        with self.assertRaises(ValueError):
            dispatch('generate_design_spec', {'project_name': 'bad', 'style': 'javascript:alert(1)'})

    def test_ui_title_is_html_escaped(self):
        title = '<img src=x onerror=alert(1)>\"'
        index = Path(create_ui_prototype('XSS test', title=title)['index'])
        text = index.read_text(encoding='utf-8')
        self.assertIn('&lt;img', text)
        self.assertNotIn(title, text)

    def test_queue_rejects_shell_dispatch_and_excessive_payloads(self):
        inbox = Path(self.workspace.name) / 'queue' / 'inbox'
        inbox.mkdir(parents=True)
        (inbox / 'malicious.json').write_text(json.dumps({'tool': 'shell', 'arguments': {'command': 'echo 1'}}))
        (inbox / 'oversized.json').write_bytes(b' ' * (MAX_TASK_BYTES + 1))
        report = process_once()
        self.assertEqual(len(report), 2)
        self.assertTrue(all(item['status'] == 'failed' for item in report))
        self.assertEqual(len(list((inbox.parent / 'failed').glob('*.result.json'))), 2)

    def test_queue_rejects_symlink(self):
        inbox = Path(self.workspace.name) / 'queue' / 'inbox'
        inbox.mkdir(parents=True)
        outside = Path(self.workspace.name) / 'external.json'
        outside.write_text('{}')
        (inbox / 'linked.json').symlink_to(outside)
        result = process_once()
        self.assertEqual(result[0]['status'], 'rejected-symlink')
        self.assertEqual(outside.read_text(), '{}')


class GeometryTests(Fixture):
    def test_city_scene_is_real_glb(self):
        r = create_city_blockout('Проект-Город', 2, 4)
        self.assertEqual(Path(r['file']).read_bytes()[:4], b'glTF')
        audit = audit_3d(r['file'])
        self.assertTrue(audit['structurally_valid'], audit['issues'])
        self.assertGreater(audit['triangles'], 100)

    def test_vehicle_models_are_real_structural_glbs(self):
        for kind in ('sports-car', 'airliner'):
            with self.subTest(kind=kind):
                r = create_vehicle_blockout(f'Набор {kind}', kind)
                audit = audit_3d(r['file'])
                self.assertTrue(audit['structurally_valid'], audit['issues'])
                self.assertGreater(audit['mesh_count'], 10)
                self.assertEqual(audit['visual_fidelity'], 'NOT TESTED')
                self.assertFalse(r['pbr_textures'])

    def test_winter_forest_is_real_glb(self):
        r = create_winter_environment('Snow', 8, seed=3)
        audit = audit_3d(r['file'])
        self.assertTrue(audit['structurally_valid'], audit['issues'])
        self.assertGreater(audit['triangles'], 300)
        self.assertEqual(r['tree_count'], 8)
        self.assertFalse(r['fps_verified'])

    def test_invalid_forest_size_rejected(self):
        for count in (0, 151, True, -1):
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    create_winter_environment('Forest invalid', count)

    def test_bad_3d_input_rejected(self):
        non_glb = Path(self.workspace.name) / 'image.png'
        non_glb.write_bytes(b'PNG')
        with self.assertRaises(ValueError):
            audit_3d(str(non_glb))


class ScreenshotTests(Fixture):
    def test_exact_match(self):
        from PIL import Image
        image = Path(self.workspace.name) / 'pic.png'
        Image.new('RGB', (32, 32), '#334455').save(image)
        result = compare_screenshots(str(image), str(image))
        self.assertEqual(result['normalized_mean_absolute_error'], 0)
        self.assertTrue(result['exact_match'])
        self.assertTrue(Path(result['difference_image']).exists())

    def test_pixel_difference_and_mismatch(self):
        from PIL import Image
        a, b = (Path(self.workspace.name) / n for n in ('a.png', 'b.png'))
        Image.new('RGB', (20, 20), '#000000').save(a)
        Image.new('RGB', (20, 20), '#FFFFFF').save(b)
        score = compare_screenshots(str(a), str(b))
        self.assertEqual(score['normalized_mean_absolute_error'], 1.0)
        self.assertFalse(score['exact_match'])
        Image.new('RGB', (21, 21), '#000000').save(b)
        with self.assertRaises(ValueError):
            compare_screenshots(str(a), str(b))


class ProtocolTests(Fixture):
    def test_stdio_roundtrip(self):
        messages = [
            'not-json',
            json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-03-26'}}),
            json.dumps({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list', 'params': {}}),
            json.dumps({'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'toolchain_probe', 'arguments': {}}}),
            json.dumps({'jsonrpc': '2.0', 'id': 4, 'method': 'tools/call', 'params': {'name': 'not-a-tool', 'arguments': {}}}),
            json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}),
        ]
        result = subprocess.run(
            [sys.executable, str(SERVER / 'mcp_server.py')],
            input='\n'.join(messages) + '\n', capture_output=True, text=True,
            timeout=15, check=True,
        )
        output = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(len(output), 5)
        self.assertEqual(output[0]['error']['code'], -32700)
        self.assertEqual(output[1]['result']['protocolVersion'], '2025-03-26')
        tool_names = {t['name'] for t in output[2]['result']['tools']}
        self.assertEqual(len(tool_names), len(TOOLS))
        self.assertFalse(output[3]['result']['isError'])
        self.assertTrue(output[4]['result']['isError'])

    def test_schema_has_valid_objects(self):
        for tool in TOOLS:
            with self.subTest(name=tool['name']):
                schema = tool['inputSchema']
                self.assertEqual(schema['type'], 'object')
                self.assertIsInstance(schema['properties'], dict)
                for req in schema.get('required', []):
                    self.assertIn(req, schema['properties'])


class OptionalBrowserTests(Fixture):
    @unittest.skipUnless(os.environ.get('VF_RUN_BROWSER_TESTS') == '1', 'Run with VF_RUN_BROWSER_TESTS=1')
    def test_responsive_ui_and_live_interactions(self):
        p = create_ui_prototype('Browser regression', 'cinematic')['index']
        report = audit_ui(p, 'browser-check')
        self.assertTrue(report['structural_checks_passed'], report)
        self.assertEqual(report['ui_interaction_smoke_test'], 'passed')
        self.assertEqual(len(report['screenshots']), 5)


if __name__ == '__main__':
    unittest.main()
