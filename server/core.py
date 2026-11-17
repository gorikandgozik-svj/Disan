"""VIBE VISUAL FORGE - local, non-fictitious visual production utilities.

No network, paid API, secrets or heavyweight binary bundled. Uses optional
Playwright/Pillow/trimesh and external Blender when installed. Explicitly
labels generated geometry as *blockout* tier, never photoreal asset.
"""
from __future__ import annotations
import html
import hashlib
import unicodedata
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STYLES={
 'dark-luxury': dict(bg='#0D111C',surface='#171C28',surface2='#242A35',text='#F4F2EF',muted='#9199A8',accent='#F4BD73',secondary='#5DE2BA',border='#434958',glow='rgba(245,184,103,.23)'),
 'tactile-glass':dict(bg='#342A2B',surface='#624848',surface2='#8B6458',text='#FFF7F1',muted='#E9C8B6',accent='#FFC59A',secondary='#FCE6CC',border='#C99A83',glow='rgba(255,201,160,.26)'),
 'cinematic':dict(bg='#0F2735',surface='#142D3C',surface2='#214256',text='#F0FBFF',muted='#AAC6D0',accent='#4CE0D4',secondary='#FFA978',border='#4A7186',glow='rgba(76,224,212,.28)'),
 'precision':dict(bg='#F0F1F3',surface='#FFFFFF',surface2='#E7E9EC',text='#171923',muted='#737784',accent='#171923',secondary='#7B88A6',border='#D6DAE1',glow='rgba(26,30,35,.12)'),
 'illustrated':dict(bg='#101C3A',surface='#1B3556',surface2='#2E4E70',text='#F1F6FF',muted='#ADC5E2',accent='#83DCEB',secondary='#F2A37A',border='#59708D',glow='rgba(125,216,235,.24)')
}

def root_dir():
    value=os.environ.get('VF_WORKSPACE_DIR')
    root=Path(value).expanduser().resolve() if value else Path.home().resolve()/'VisualForgeProjects'
    root.mkdir(parents=True,exist_ok=True)
    return root

def slug(name):
    """Stable, safe and collision-resistant directory key for non-ASCII names."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError('project name must be a nonempty string')
    if len(name) > 160:
        raise ValueError('project name is too long')
    normalized = unicodedata.normalize('NFKD', name.strip())
    ascii_name = normalized.encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-z0-9_-]+', '-', ascii_name.lower()).strip('-')[:48]
    if not value:
        value = 'project'
    # Prevent Cyrillic / Chinese / emoji-only names collapsing to "project".
    digest = hashlib.sha256(name.encode('utf-8')).hexdigest()[:10]
    return value + '-' + digest

def project_dir(name):
    d=root_dir()/slug(name)
    d.mkdir(parents=True,exist_ok=True)
    return d

def probe():
    binaries={n:shutil.which(n) for n in ['python','node','npm','blender','godot','ffmpeg','chromium','google-chrome','gradle']}
    imports={n:__import__('importlib.util',fromlist=['find_spec']).find_spec(n) is not None for n in ['PIL','trimesh','playwright','pytest']}
    return {'platform':platform.platform(),'python':sys.version.split()[0],'executables':binaries,'python_modules':imports,'workspace':str(root_dir()),'cloud_render_available':False,'scope':'local-process only'}

def analyze_reference(image_path):
    from PIL import Image, ImageStat
    p=Path(image_path).expanduser().resolve()
    if not p.is_file() or p.suffix.lower() not in ('.png','.jpeg','.jpg','.webp'):
        raise ValueError('A local PNG/JPEG/WEBP file is required')
    if p.stat().st_size > 25 * 1024 * 1024:
        raise ValueError('Reference exceeds 25 MiB limit')
    with Image.open(p) as source:
        if source.width * source.height > 40_000_000:
            raise ValueError('Reference exceeds 40 megapixels limit')
        img=source.convert('RGB')
        size=img.size
        img.thumbnail((192,192))
        pal=img.quantize(colors=7,method=Image.Quantize.MEDIANCUT).convert('RGB')
        colors=pal.getcolors(pal.width*pal.height)
        top=sorted(colors,key=lambda x:-x[0])[:7]
        st=ImageStat.Stat(img)
        return {'reference':str(p),'width':size[0],'height':size[1],
          'dominant_rgb_hex':['#%02X%02X%02X'%tuple(c) for _,c in top],
          'mean_rgb':[round(v,1) for v in st.mean],
          'warning':'Color/pixel measurements only; no semantic understanding or 3D reconstruction'}

def generate_spec(project_name, style, target='web', brief=''):
    if style not in STYLES:raise ValueError('style must be one of '+', '.join(STYLES))
    if target not in ('web','android','desktop'):raise ValueError('target must be web/android/desktop')
    d=project_dir(project_name)
    spec={'project':project_name,'style':style,'target':target,'brief':brief,
         'design_tokens':STYLES[style],
         'reference_contract':['functional state and controls','responsive and accessible','reference comparison after rendering','no screenshot-as-app substitution'],
         'assets_verified':False,'visual_fidelity_verified':False,'build_verified':False,
         'created_at':datetime.now(timezone.utc).isoformat()}
    path=d/'style-spec.json';path.write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
    return {'spec':str(path),'style':style,'target':target,'claim':'design specification, NOT a compiled application'}

TEMPLATE=r'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="__BG__"><title>__TITLE__ — Visual Console</title><style>
:root{--bg:__BG__;--surface:__SURFACE__;--surface2:__SURFACE2__;--txt:__TEXT__;--muted:__MUTED__;--accent:__ACCENT__;--secondary:__SECONDARY__;--border:__BORDER__;--glow:__GLOW__}
*{box-sizing:border-box}html{font-family:Inter,ui-sans-serif,system-ui,Arial,sans-serif;color:var(--txt);background:var(--bg)}body{margin:0;min-height:100vh;background:radial-gradient(ellipse 60% 45% at 75% -12%,var(--glow),transparent 82%),radial-gradient(ellipse 50% 65% at -22% 106%,var(--glow),transparent 80%),var(--bg);letter-spacing:-.012em}
button,input,select{font:inherit}button{cursor:pointer}button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid var(--secondary);outline-offset:3px}button:disabled{opacity:.4;cursor:not-allowed}.shell{max-width:1470px;margin:auto;display:grid;grid-template-columns:240px minmax(0,1fr);min-height:100vh;gap:32px;padding:22px 30px 50px 22px}
.sidebar{background:linear-gradient(130deg,color-mix(in srgb,var(--surface),transparent 2%),color-mix(in srgb,var(--surface),transparent 24%));border:1px solid color-mix(in srgb,var(--border),transparent 35%);border-radius:24px;padding:27px 17px;display:flex;flex-direction:column;gap:28px;box-shadow:0 22px 65px rgba(0,0,0,.12)}.brand{display:flex;align-items:center;gap:12px;padding-left:12px;font-size:15px;letter-spacing:.12em;font-weight:750}.mark{width:35px;height:35px;border-radius:12px;background:linear-gradient(135deg,var(--secondary),var(--accent));color:#121620;font-size:25px;display:grid;place-items:center;box-shadow:0 6px 24px var(--glow)}.tiny{color:var(--muted);font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-weight:700;margin:4px 12px -16px}.nav{display:grid;gap:6px}.nav button{width:100%;padding:13px 14px;color:var(--muted);display:flex;align-items:center;gap:13px;border:0;background:transparent;border-radius:14px;text-align:left}.nav button[aria-pressed=true],.nav button:hover{color:var(--txt);background:var(--surface2)}.nav b{width:24px;text-align:center;color:var(--accent)}.sidebar-footer{margin-top:auto;padding:17px;background:var(--surface2);border-radius:17px;font-size:12px;line-height:1.6;color:var(--muted)}.sidebar-footer strong{color:var(--txt);display:block;font-size:14px}
main{min-width:0;padding-top:16px}.top{display:flex;justify-content:space-between;gap:20px;align-items:center}.eyebrow{font-size:11px;color:var(--accent);font-weight:700;letter-spacing:.2em;text-transform:uppercase}.top h1{font-size:clamp(27px,3vw,44px);line-height:1.08;margin:10px 0 9px;letter-spacing:-.055em;font-weight:650}.sub{color:var(--muted);font-size:14px;margin:0}.actions{display:flex;align-items:center;gap:12px}.avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(145deg,var(--secondary),var(--accent));box-shadow:0 0 0 5px var(--surface);color:#131924;display:grid;place-items:center;font-weight:800}.btn{border:1px solid var(--border);border-radius:12px;padding:11px 16px;color:var(--txt);background:var(--surface2);transition:transform .18s,box-shadow .18s}.btn:hover{transform:translateY(-2px);box-shadow:0 8px 22px var(--glow)}.btn.primary{background:var(--accent);color:#151923;border-color:transparent;font-weight:750}.tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:30px 0 16px}.tile,.card{border:1px solid color-mix(in srgb,var(--border),transparent 42%);background:linear-gradient(160deg,color-mix(in srgb,var(--surface),transparent 0%),color-mix(in srgb,var(--surface),var(--bg) 13%));box-shadow:0 22px 60px rgba(0,0,0,.12);border-radius:22px}.tile{padding:23px;min-width:0}.tile p{font-size:12px;color:var(--muted);margin:0 0 17px}.tile strong{font-size:clamp(24px,2.5vw,34px);line-height:1;letter-spacing:-.05em;font-weight:690}.delta{font-size:12px;color:var(--secondary);margin-top:14px}.content{display:grid;grid-template-columns:minmax(0,1.75fr) minmax(0,1fr);gap:16px}.card{padding:24px;min-width:0}.card h2{font-size:17px;font-weight:620;letter-spacing:-.03em;margin:0}.card small{color:var(--muted)}.card-top{display:flex;align-items:start;justify-content:space-between;gap:14px}.hero{height:290px;margin-top:25px;overflow:hidden;border-radius:19px;position:relative;background:linear-gradient(160deg,color-mix(in srgb,var(--accent),var(--surface) 65%) -30%,var(--surface) 48%,color-mix(in srgb,var(--secondary),var(--bg) 66%))}.hero:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 65% 30%,color-mix(in srgb,var(--accent),transparent 54%),transparent 35%)}.mountain{position:absolute;bottom:-2px;width:150%;left:-23%;height:72%;filter:drop-shadow(0 22px 20px rgba(0,0,0,.27))}.mountain path:first-child{fill:color-mix(in srgb,var(--secondary),var(--bg) 45%)}.mountain path:nth-child(2){fill:color-mix(in srgb,var(--accent),var(--bg) 50%)}.mountain path:nth-child(3){fill:color-mix(in srgb,var(--surface2),var(--bg) 18%)}.hero-label{position:absolute;left:25px;top:25px;font-size:12px;letter-spacing:.11em;text-transform:uppercase;font-weight:700}.hero-stat{position:absolute;bottom:22px;left:25px;z-index:2;font-size:13px;color:var(--txt)}.hero-stat b{font-size:32px;display:block;margin-bottom:2px}.graph{width:100%;height:167px;margin-top:28px;overflow:visible}.graph .gridline{stroke:var(--border);stroke-width:1;opacity:.42}.graph .line{stroke:var(--accent);stroke-width:3;fill:none;stroke-linejoin:round;stroke-linecap:round}.graph .area{fill:var(--glow)}.axis{display:flex;justify-content:space-between;color:var(--muted);font-size:11px}.bar-group{display:flex;align-items:end;gap:13px;height:142px;margin-top:25px}.bar{flex:1;max-width:54px;height:var(--bar);border-radius:8px 8px 3px 3px;background:linear-gradient(0deg,color-mix(in srgb,var(--accent),var(--surface2) 17%),var(--secondary));opacity:.92}.below{display:grid;grid-template-columns:minmax(0,1.75fr) minmax(0,1fr);gap:16px;margin-top:16px}.slider-row{display:flex;gap:20px;align-items:center;margin:24px 0 10px}.slider-row input{min-width:0;flex:1;accent-color:var(--accent)}.large{font-size:30px;font-weight:720;letter-spacing:-.05em}.switch{position:relative;display:inline-flex;align-items:center;gap:12px;cursor:pointer;user-select:none}.switch input{width:20px;height:20px;accent-color:var(--accent)}.status{color:var(--muted);font-size:12px;line-height:1.55;margin-top:18px}.accent{color:var(--accent)}.status[role=status]{min-height:19px}.footer{color:var(--muted);font-size:11px;margin-top:23px;display:flex;justify-content:space-between;gap:10px}.hide{display:none!important}
@media(max-width:1050px){.shell{grid-template-columns:80px minmax(0,1fr);padding:14px;gap:15px}.sidebar{padding:20px 10px;align-items:stretch}.brand{justify-content:center;padding:0}.brand span,.nav button span,.tiny,.sidebar-footer{display:none}.nav button{justify-content:center}.tiles{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){.shell{display:block;padding:12px 14px 32px}.sidebar{border-radius:18px;padding:10px 14px;flex-direction:row;align-items:center;gap:18px;min-height:0}.brand{flex:none}.nav{display:flex;flex:1;justify-content:space-around}.nav button{padding:11px;min-width:40px}.top{margin-top:24px;align-items:start}.top h1{font-size:31px}.actions .btn{padding:9px 11px;font-size:12px}.avatar{height:38px;width:38px}.tiles{gap:10px;margin-top:23px}.tile,.card{padding:17px;border-radius:18px}.tile strong{font-size:26px}.content,.below{grid-template-columns:minmax(0,1fr)}.hero{height:245px;margin-top:17px}.bar-group{height:110px}.footer{flex-direction:column}main{padding-top:0}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{transition:none!important;animation:none!important}}
</style></head><body><div class="shell">
<aside class="sidebar"><div class="brand"><div class="mark" aria-label="Vibe Visual Forge logo">◇</div><span>VIBE / FORGE</span></div><p class="tiny">Workspace</p><nav class="nav" aria-label="Main menu"><button aria-label="Overview" aria-pressed="true" data-tab="dashboard"><b>◈</b><span>Overview</span></button><button aria-label="Analytics" aria-pressed="false" data-tab="analytics"><b>⌁</b><span>Analytics</span></button><button aria-label="Scenes" aria-pressed="false" data-tab="scenes"><b>▤</b><span>Scenes</span></button><button aria-label="Settings" aria-pressed="false" data-tab="settings"><b>⚙</b><span>Settings</span></button></nav><div class="sidebar-footer"><strong>Visual prototype</strong>Local interactive interface. No cloud AI connected.</div></aside>
<main><header class="top"><div><div class="eyebrow">Design systems / Studio Preview</div><h1>__TITLE__</h1><p class="sub" id="subtitle">Performance, visuals and creative control in one workspace.</p></div><div class="actions"><button class="btn" id="reset">Reset</button><div class="avatar" aria-label="User avatar">VF</div></div></header>
<section class="tiles" aria-label="Project overview"><article class="tile"><p>Visual components</p><strong>128</strong><div class="delta">● Library available</div></article><article class="tile"><p>Interactive states</p><strong id="states">24</strong><div class="delta">● Running locally</div></article><article class="tile"><p>Assets in library</p><strong>723</strong><div class="delta">◈ Sample data</div></article><article class="tile"><p>Lighting intensity</p><strong id="light-tile">64%</strong><div class="delta">↗ Live control</div></article></section>
<section class="content"><article class="card"><div class="card-top"><div><h2>Atmospheric viewport</h2><small>Procedural SVG illustration, not a photoreal 3D render</small></div><button class="btn" id="scene-btn">Change mood</button></div><div class="hero" id="hero"><div class="hero-label">__SCENE_LABEL__</div><svg class="mountain" viewBox="0 0 1200 450" preserveAspectRatio="none" aria-label="Stylized mountain layers"><path d="M0,260 L80,170 160,210 300,35 425,200 560,100 700,260 830,125 950,270 1100,160 1200,290 1200,450 0,450Z"/><path d="M0,300 L140,220 240,275 385,125 535,320 655,200 800,345 935,220 1020,298 1200,240 1200,450 0,450Z"/><path d="M0,370 L110,255 210,365 390,255 520,390 690,280 835,405 1020,280 1200,375 1200,450 0,450Z"/></svg><div class="hero-stat"><b id="hero-value">DUSK 18:42</b>Environment lighting profile</div></div><div class="footer"><span>Editable layers · responsive layout</span><span class="accent" id="mood">Warm dusk</span></div></article>
<article class="card"><div class="card-top"><div><h2>Activity signal</h2><small>Live adjustable chart sample</small></div><span class="eyebrow">7 days</span></div><svg viewBox="0 0 330 168" class="graph" preserveAspectRatio="none" aria-label="Activity chart" role="img"><path class="gridline" d="M0 40H330 M0 90H330 M0 140H330"/><path class="area" d="M0 125L40 108 80 114 120 78 160 93 200 40 240 58 280 24 330 36V168H0Z"/><path class="line" d="M0 125L40 108 80 114 120 78 160 93 200 40 240 58 280 24 330 36"/></svg><div class="axis"><span>MON</span><span>TUE</span><span>WED</span><span>THU</span><span>FRI</span><span>SAT</span><span>SUN</span></div><div class="bar-group" aria-label="Bar chart"><div class="bar" style="--bar:61%"></div><div class="bar" style="--bar:82%"></div><div class="bar" style="--bar:44%"></div><div class="bar" style="--bar:72%"></div><div class="bar" style="--bar:100%"></div><div class="bar" style="--bar:76%"></div><div class="bar" style="--bar:88%"></div></div><p class="status">Illustrative values. Connect a real data source before production use.</p></article></section>
<section class="below"><article class="card"><div class="card-top"><div><h2>Lighting studio</h2><small>Functional slider and switch</small></div><label class="switch"><input type="checkbox" checked id="light-enabled"><span>Enabled</span></label></div><div class="slider-row"><input aria-label="Lighting intensity" id="light" type="range" min="0" max="100" value="64"><span class="large" id="light-value">64%</span></div><div class="status" id="status" role="status" aria-live="polite">Light at 64%. Controls are interactive.</div></article><article class="card"><div class="card-top"><div><h2>Material mode</h2><small>Working appearance switcher</small></div></div><div class="slider-row"><select class="btn" id="mode" aria-label="Material mode" style="max-width:100%;width:100%"><option value="Warm dusk">Warm dusk</option><option value="Cold alpine">Cold alpine</option><option value="Studio glow">Studio glow</option></select></div><p class="status">A visual interaction sample. No geometry, Blender render or model synthesis is performed by this page.</p></article></section>
<div class="footer"><span>VIBE VISUAL FORGE · Functional web UI prototype</span><span>Static sample data · No fake backend</span></div></main></div>
<script>
const q=s=>document.querySelector(s);const light=q('#light'),lightVal=q('#light-value'),tile=q('#light-tile'),enabled=q('#light-enabled'),stat=q('#status'),mode=q('#mode');
function refresh(){const v=enabled.checked?Number(light.value):0;lightVal.textContent=v+'%';tile.textContent=v+'%';light.disabled=!enabled.checked;stat.textContent=enabled.checked?'Light at '+v+'%. Controls are interactive.':'Lighting disabled.';q('#hero').style.filter='brightness('+(0.68+v/200)+') hue-rotate('+getComputedStyle(q('#hero')).getPropertyValue('--mood-rotation').trim()+')'}
light.addEventListener('input',refresh);enabled.addEventListener('change',refresh);
function mood(v){q('#mood').textContent=v;mode.value=v;q('#hero-value').textContent=v==='Warm dusk'?'DUSK 18:42':v==='Cold alpine'?'ALPINE 06:25':'STUDIO 20:17';q('#hero').style.setProperty('--mood-rotation',v==='Cold alpine'?'95deg':v==='Studio glow'?'215deg':'0deg');refresh();refresh();}
mode.addEventListener('change',()=>mood(mode.value));q('#scene-btn').addEventListener('click',()=>{const vs=['Warm dusk','Cold alpine','Studio glow'];mood(vs[(vs.indexOf(mode.value)+1)%vs.length]);});
q('#reset').addEventListener('click',()=>{enabled.checked=true;light.value=64;mood('Warm dusk');q('#status').textContent='All controls reset.';});
document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-tab]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));q('#subtitle').textContent={dashboard:'Performance, visuals and creative control in one workspace.',analytics:'Analytics view selected. Sample values remain illustrative.',scenes:'Scenes view selected. Edit the environmental mood below.',settings:'Settings view selected. Try controls in Lighting studio.'}[b.dataset.tab];}));refresh();
</script></body></html>'''

def create_ui_prototype(project_name,style='dark-luxury',title=None):
    if style not in STYLES:raise ValueError('Unknown style')
    if not project_name or len(project_name)>100:raise ValueError('Invalid project name')
    d=project_dir(project_name); t=title or project_name
    txt=TEMPLATE.replace('__TITLE__',html.escape(t,quote=True)).replace('__SCENE_LABEL__',html.escape(style.replace('-',' ')))
    mapping={'BG':'bg','SURFACE':'surface','SURFACE2':'surface2','TEXT':'text','MUTED':'muted','ACCENT':'accent','SECONDARY':'secondary','BORDER':'border','GLOW':'glow'}
    for tag,k in mapping.items():txt=txt.replace('__'+tag+'__',STYLES[style][k])
    (d/'index.html').write_text(txt,encoding='utf-8')
    spec=generate_spec(project_name,style,'web','Interactive *demo*, not a compiled Android/Windows application')
    return {'index':str(d/'index.html'),'spec':spec['spec'],'framework':'HTML/CSS/JS','actual_interactions':['slider','switch','tabs','mood','reset'],'limitations':['sample chart data','SVG illustrated background is not a 3D mesh','not photoreal','not APK/EXE'],'project_tier':'functional web UI prototype'}

def audit_ui(index_path, output_name='audit'):
    from playwright.sync_api import sync_playwright
    p=Path(index_path).expanduser().resolve()
    if not p.is_file() or p.suffix.lower()!='.html':raise ValueError('Existing local HTML file required')
    out=project_dir(output_name); results=[]
    with sync_playwright() as pw:
      b=None
      try:
        try:b=pw.chromium.launch(headless=True,executable_path=shutil.which('chromium') or shutil.which('google-chrome'))
        except Exception:b=pw.chromium.launch(headless=True)
        for width,height in [(320,568),(390,844),(768,1024),(832,384),(1440,900)]:
          page=b.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
          errors=[]
          page.on('pageerror',lambda error:errors.append(str(error)))
          page.route('**/*', lambda route: route.abort())  # local QA never fetches external assets
          page.set_content(p.read_text(encoding="utf8"),wait_until="load")
          page.wait_for_timeout(180)
          shot=out/f'{width}x{height}.png';page.screenshot(path=str(shot),full_page=True)
          metrics=page.evaluate('''() => ({ scrollWidth:document.documentElement.scrollWidth, clientWidth:document.documentElement.clientWidth, controls:document.querySelectorAll('button, input, select').length, bodyText:document.body.innerText.length, invalidTargets:[...document.querySelectorAll('button')].filter(e=>{const r=e.getBoundingClientRect();return getComputedStyle(e).display!=='none'&&(r.width<32||r.height<32)}).length})''')
          metrics.update({'viewport':[width,height], 'screenshot':str(shot),'js_errors':errors, 'horizontal_overflow':metrics['scrollWidth']>metrics['clientWidth']+2})
          metrics['semantic_main']=page.locator('main').count()==1
          metrics['has_page_title']=bool(page.locator('h1').inner_text().strip())
          metrics['missing_button_names']=page.evaluate('''() => [...document.querySelectorAll('button')].filter(el => el.getClientRects().length && !(el.getAttribute('aria-label') || el.innerText).trim()).length''')
          metrics['passed_structural_checks']=not errors and not metrics['horizontal_overflow'] and metrics['invalidTargets']==0 and metrics['semantic_main'] and metrics['has_page_title'] and metrics['missing_button_names']==0
          results.append(metrics)
          if width==390:
            page.locator('#light').fill('42')
            if page.locator('#light-value').inner_text()!='42%':raise RuntimeError('Slider functional test failed')
            page.locator('#scene-btn').click()
            if page.locator('#mood').inner_text()!='Cold alpine':raise RuntimeError('Scene switch failed')
            page.locator('[data-tab=analytics]').click()
            if page.locator('[data-tab=analytics]').get_attribute('aria-pressed')!='true':raise RuntimeError('Navigation state failed')
            page.locator('#reset').click()
            if page.locator('#light-value').inner_text()!='64%':raise RuntimeError('Reset state failed')
          page.close()
      finally:
        if b:b.close()
    report={'screenshots':results,'structural_checks_passed':all(r['passed_structural_checks'] for r in results),'ui_interaction_smoke_test':'passed','aesthetic_review':'NOT TESTED: requires visual/reference review','performance_mobile_device':'NOT TESTED'}
    path=out/'report.json';path.write_text(json.dumps(report,indent=2),encoding='utf8')
    report['report']=str(path)
    return report


def compare_screenshots(reference_path, rendered_path, output_name='comparison'):
    """Pixel-space difference for two screenshots. Not a semantic aesthetics score."""
    from PIL import Image, ImageChops, ImageStat
    p1 = Path(reference_path).expanduser().resolve()
    p2 = Path(rendered_path).expanduser().resolve()
    for path in (p1, p2):
        if not path.is_file() or path.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp'):
            raise ValueError('Existing PNG or JPEG/WEBP images required')
        if path.stat().st_size > 25 * 1024 * 1024:
            raise ValueError('Screenshot exceeds 25 MiB')
    with Image.open(p1) as original, Image.open(p2) as candidate:
        if max(original.width * original.height, candidate.width * candidate.height) > 20_000_000:
            raise ValueError('Screenshot exceeds 20 megapixels')
        if original.size != candidate.size:
            raise ValueError('Screenshot dimensions must match; do not stretch a reference')
        ref = original.convert('RGB')
        comp = candidate.convert('RGB')
        difference = ImageChops.difference(ref, comp)
        stats = ImageStat.Stat(difference)
        normalized_mae = sum(stats.mean) / (3.0 * 255.0)
        path = project_dir(output_name) / 'pixel-diff.png'
        difference.save(path)
        return {'reference': str(p1), 'rendered': str(p2),
                'size': list(ref.size), 'normalized_mean_absolute_error': round(normalized_mae, 6),
                'exact_match': difference.getbbox() is None, 'difference_image': str(path),
                'meaning': 'Raw pixel difference only; cannot validate semantic or physical quality'}

def create_city_blockout(project_name, blocks=4, seed=14):
    import random
    import trimesh
    if not 1<=int(blocks)<=9:raise ValueError('blocks must be 1..9')
    r=random.Random(int(seed));s=trimesh.Scene();unit=28.0
    def box(name,extents,xyz,col):
        obj=trimesh.creation.box(extents=extents);obj.apply_translation(xyz)
        obj.visual.face_colors=col;s.add_geometry(obj,geom_name=name)
    box('terrain',(blocks*unit+30,blocks*unit+30,.4),(0,0,-.3),(94,117,97,255))
    palette=[(97,103,111,255),(138,124,105,255),(179,145,109,255),(117,138,148,255),(109,120,136,255)]
    for i in range(blocks):
      for j in range(blocks):
        x=(i-(blocks-1)/2)*unit;y=(j-(blocks-1)/2)*unit
        for ix in [-1,0,1]:
          for iy in [-1,0,1]:
            a=x+ix*6.4;b=y+iy*6.4;h=r.uniform(7,38)*(.6 if (i+j)%3==0 else 1.0)
            box(f'building-{i}-{j}-{ix}-{iy}',(4.4,4.4,h),(a,b,h/2),r.choice(palette))
            box(f'roof-{i}-{j}-{ix}-{iy}',(4.0,4.0,.5),(a,b,h+.3),(72,77,82,255))
            if r.random()>.55:
              box(f'roof-unit-{i}-{j}-{ix}-{iy}',(2,1.5,1.1),(a+.1,b-.2,h+1.1),(131,131,127,255))
    for k in range(blocks+1):
        center=(k-blocks/2)*unit-unit/2
        box(f'road-east-{k}',(blocks*unit+24,5,.08),(0,center,0.01),(57,61,68,255))
        box(f'road-north-{k}',(5,blocks*unit+24,.08),(center,0,.01),(57,61,68,255))
    out=project_dir(project_name);p=out/'city-blockout.glb';p.write_bytes(s.export(file_type='glb'))
    info={'project':project_name,'file':str(p),'geometry_count':len(s.geometry),'format':'GLB','tier':'BLOCKOUT, not photoreal or complete game','scale':'meters (approximate)','textures':'basic vertex colors, no image textures','seed':int(seed),'blocks':int(blocks),'engine_import_tested':False}
    (out/'3d-report.json').write_text(json.dumps(info,indent=2),encoding='utf8')
    return info

BLENDER_RECIPE=r'''# Generated by VIBE VISUAL FORGE. Requires Blender 4.x and source GLB.
# Usage: blender --background --python studio_render.py -- /absolute/path/model.glb
import bpy, sys, math
from mathutils import Vector
from pathlib import Path
args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if not args: raise SystemExit('Provide a real, sourced local GLB model path')
source=Path(args[0]); assert source.is_file() and source.suffix.lower()=='.glb', 'GLB missing'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(source))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
assert meshes,'No meshes imported'
# Normalization is intentionally NOT automatic: preserve model scale.
world=bpy.context.scene.world or bpy.data.worlds.new('Studio World');bpy.context.scene.world=world
world.use_nodes=True;world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.11,.13,.17,1)
world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.55
for name,loc,power,size,color in [('Key',(7,-6,12),1600,8,(1,.81,.63)),('Fill',(-8,-3,7),950,7,(.59,.77,1)),('Rim',(1,8,10),2100,5,(1,1,1))]:
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;data.color=color
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj);obj.location=loc
    direction=Vector((0,0,0))-obj.location;obj.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
cam_data=bpy.data.cameras.new('Studio Camera');cam=bpy.data.objects.new('Studio Camera',cam_data)
bpy.context.collection.objects.link(cam);cam.location=(10,-12,8)
cam.rotation_euler=(Vector((0,0,1.2))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.scene.camera=cam;cam_data.type='ORTHO';cam_data.ortho_scale=16
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=64
sc.render.resolution_x=1600;sc.render.resolution_y=900;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG';sc.render.filepath=str(source.with_name('studio-render.png'))
bpy.ops.render.render(write_still=True)
print('Rendered',sc.render.filepath)
'''

def create_blender_recipe(project_name):
    d=project_dir(project_name);p=d/'studio_render.py';p.write_text(BLENDER_RECIPE,encoding='utf8')
    return {'script':str(p),'requires':'Blender 4.x, user-supplied GLB, source material/texture assets','rendered':False,'claim':'ready-to-run studio render recipe, not a completed render'}

TOOLS=[
 {'name':'toolchain_probe','description':'Detect local graphic and build dependencies and workspace; no install or network access','inputSchema':{'type':'object','properties':{}}},
 {'name':'analyze_reference','description':'Analyze local reference PNG/JPEG dominant palette and dimensions; no semantic model','inputSchema':{'type':'object','required':['image_path'],'properties':{'image_path':{'type':'string'}}}},
 {'name':'generate_design_spec','description':'Write tokens and acceptance criteria for style, not a compiled app','inputSchema':{'type':'object','required':['project_name','style'],'properties':{'project_name':{'type':'string'},'style':{'type':'string','enum':list(STYLES)},'target':{'type':'string','enum':['web','desktop','android']},'brief':{'type':'string'}}}},
 {'name':'create_ui_prototype','description':'Build actual functional responsive HTML/CSS/JS prototype with interactive controls; NOT APK/EXE','inputSchema':{'type':'object','required':['project_name'],'properties':{'project_name':{'type':'string'},'style':{'type':'string','enum':list(STYLES)},'title':{'type':'string'}}}},
 {'name':'audit_ui','description':'Use Playwright/Chrome to screenshot 3 widths and verify overflow and interactions','inputSchema':{'type':'object','required':['index_path'],'properties':{'index_path':{'type':'string'},'output_name':{'type':'string'}}}},
 {'name':'create_city_blockout','description':'Generate an importable procedural GLB 3D city BLOCKOUT; not high-detail photoreal environment','inputSchema':{'type':'object','required':['project_name'],'properties':{'project_name':{'type':'string'},'blocks':{'type':'integer','minimum':1,'maximum':9},'seed':{'type':'integer'}}}},
 {'name':'create_blender_recipe','description':'Write a Blender Cycles studio render recipe for a user-provided GLB; Blender execution separate','inputSchema':{'type':'object','required':['project_name'],'properties':{'project_name':{'type':'string'}}}},
 {'name':'create_vehicle_blockout','description':'Create a named-part real GLB sports-car or airliner geometric blockout (not photoreal or accurate CAD)','inputSchema':{'type':'object','required':['project_name'],'properties':{'project_name':{'type':'string'},'vehicle_type':{'type':'string','enum':['sports-car','airliner']}}}},
 {'name':'create_winter_environment','description':'Generate real low-poly snowy forest GLB blockout (no photorealism or FPS claim)','inputSchema':{'type':'object','required':['project_name'],'properties':{'project_name':{'type':'string'},'tree_count':{'type':'integer','minimum':1,'maximum':150},'seed':{'type':'integer'}}}},
 {'name':'compare_screenshots','description':'Compute pixel-difference image for equal-size screenshots; not aesthetic equivalence','inputSchema':{'type':'object','required':['reference_path','rendered_path'],'properties':{'reference_path':{'type':'string'},'rendered_path':{'type':'string'},'output_name':{'type':'string'}}}},
 {'name':'audit_3d','description':'Check real GLB triangle geometry, bounds and invalid faces; no visual quality/FPS assertions','inputSchema':{'type':'object','required':['glb_path'],'properties':{'glb_path':{'type':'string'}}}}
]

def dispatch(name, args):
    args=args or {}
    from procedural_assets import create_vehicle_blockout, audit_3d, create_winter_environment
    handlers={'toolchain_probe':probe,'analyze_reference':analyze_reference,'generate_design_spec':generate_spec,'create_ui_prototype':create_ui_prototype,'audit_ui':audit_ui,'create_city_blockout':create_city_blockout,'create_blender_recipe':create_blender_recipe,'create_vehicle_blockout':create_vehicle_blockout,'audit_3d':audit_3d,'create_winter_environment':create_winter_environment,'compare_screenshots':compare_screenshots}
    if name not in handlers:raise ValueError(f'Unknown tool {name}')
    return handlers[name](**args)
