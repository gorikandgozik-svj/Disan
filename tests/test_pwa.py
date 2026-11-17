"""Cross-platform browser smoke tests for the PWA using local in-memory module imports.
Run with VF_RUN_BROWSER_TESTS=1 python -m unittest discover -s tests -v.
No public network is used. Service worker installation is not simulated.
"""
import base64
import json
import os
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'public'

@unittest.skipUnless(os.getenv('VF_RUN_BROWSER_TESTS')=='1','set VF_RUN_BROWSER_TESTS=1')
class TestPWA(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from playwright.sync_api import sync_playwright
  cls.pw=sync_playwright().start()
  binary=os.environ.get('VF_BROWSER_EXECUTABLE')
  cls.browser=cls.pw.chromium.launch(executable_path=binary or None,headless=True,args=['--no-sandbox'])
  html=(ROOT/'index.html').read_text(encoding='utf8')
  css=(ROOT/'css/app.css').read_text(encoding='utf8')
  cls.html=html.replace('<link rel="stylesheet" href="/css/app.css">','<style>'+css+'</style>').replace('<script type="module" src="/js/app.mjs"></script>','')
  eng=base64.b64encode((ROOT/'js/engine.mjs').read_bytes()).decode()
  app=(ROOT/'js/app.mjs').read_text(encoding='utf8').replace("from './engine.mjs'",f"from 'data:text/javascript;base64,{eng}'")
  cls.app_url='data:text/javascript;base64,'+base64.b64encode(app.encode()).decode()
 @classmethod
 def tearDownClass(cls):
  cls.browser.close();cls.pw.stop()
 def _page(self,width,height):
  p=self.browser.new_page(viewport={'width':width,'height':height});p.goto('about:blank');p.set_content(self.html)
  p.evaluate('''() => {const store={};Object.defineProperty(window,'localStorage',{value:{getItem:(k)=>store[k]??null,setItem:(k,v)=>store[k]=String(v),removeItem:(k)=>delete store[k]}})}''')
  p.evaluate('(url) => import(url)',self.app_url)
  p.frame_locator('#uiFrame').locator('h1').wait_for()
  return p
 def test_mobile_layout_and_interaction(self):
  p=self._page(390,844)
  try:
   self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),390)
   p.locator('#projectName').fill('Racing Studio');p.locator('#refreshPreview').click()
   self.assertEqual(p.frame_locator('#uiFrame').locator('h1').inner_text(),'Racing Studio')
   p.locator('#saveBtn').click();p.locator('[data-route="library"]').click()
   self.assertEqual(p.locator('.library-item').count(),1)
  finally:p.close()
 def test_desktop_live_3d(self):
  p=self._page(1440,900)
  try:
   self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),1440)
   p.locator('[data-route="scene"]').click();self.assertGreater(int(p.locator('#meshCount').inner_text()),30)
   p.locator('#sceneSelect').select_option('airliner')
   self.assertEqual(p.locator('#sceneLabel').inner_text(),'AIRLINER / 42')
   self.assertGreater(p.evaluate('document.querySelector("#sceneCanvas").width'),200)
  finally:p.close()
 def test_landscape_qa(self):
  p=self._page(832,384)
  try:
   self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),832)
   p.locator('[data-route="quality"]').click()
   self.assertEqual(p.locator('#contrastRatio').inner_text(),'16.60 : 1')
  finally:p.close()
