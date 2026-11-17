import json, os, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'server'))
from core import STYLES, analyze_reference, generate_spec, create_ui_prototype, create_city_blockout, create_blender_recipe, TOOLS

class TestVisualForge(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(prefix='vf-test-')
  os.environ['VF_WORKSPACE_DIR']=cls.tmp.name
 @classmethod
 def tearDownClass(cls):
  cls.tmp.cleanup()
  os.environ.pop('VF_WORKSPACE_DIR',None)
 def test_styles(self):
  self.assertEqual(len(STYLES),5)
  self.assertEqual(len({t['name'] for t in TOOLS}),11)
 def test_spec(self):
  path=Path(generate_spec('My Project','dark-luxury')['spec'])
  doc=json.loads(path.read_text(encoding='utf8'))
  self.assertFalse(doc['visual_fidelity_verified'])
 def test_ui(self):
  path=Path(create_ui_prototype('UI Example','cinematic')['index'])
  h=path.read_text()
  self.assertIn('id="light"',h)
  self.assertIn("addEventListener('input'",h)
  self.assertNotIn('__ACCENT__',h)
  self.assertGreater(len(h),8500)
 def test_3d(self):
  import trimesh
  d=create_city_blockout('City Example',2,seed=8)
  self.assertEqual(d['tier'],'BLOCKOUT, not photoreal or complete game')
  mesh=trimesh.load(d['file'],force='scene')
  self.assertGreater(len(mesh.geometry),25)
  self.assertGreater(Path(d['file']).stat().st_size,1024)
 def test_blender_recipe(self):
  p=Path(create_blender_recipe('Airplane')['script'])
  compile(p.read_text(),str(p),'exec')
 def test_analyze_reference(self):
  from PIL import Image
  p=Path(self.tmp.name)/'ref.png';Image.new('RGB',(60,80),'#AA3300').save(p)
  self.assertEqual(analyze_reference(str(p))['width'],60)

if __name__=='__main__':unittest.main()

class TestWatcher(unittest.TestCase):
 def test_queue(self):
  from watch import process_once
  import tempfile
  with tempfile.TemporaryDirectory(prefix='vf-watch-') as d:
   previous=os.environ.get('VF_WORKSPACE_DIR')
   os.environ['VF_WORKSPACE_DIR']=d
   try:
    p=Path(d)/'queue/inbox/1.json';p.parent.mkdir(parents=True)
    p.write_text(json.dumps({'tool':'create_ui_prototype','arguments':{'project_name':'Watcher Demo','style':'precision'}}))
    result=process_once()
    self.assertEqual(result[0]['status'],'completed')
    report=json.loads((Path(d)/'queue/done/1.result.json').read_text())
    self.assertEqual(report['status'],'completed')
    self.assertTrue(Path(report['result']['index']).is_file())
   finally:
    if previous:os.environ['VF_WORKSPACE_DIR']=previous
    else:os.environ.pop('VF_WORKSPACE_DIR',None)
