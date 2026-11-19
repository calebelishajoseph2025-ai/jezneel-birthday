"""Run against a running server (default http://127.0.0.1:8765). Optional: BIRTHDAY_URL and CHROMIUM_PATH."""
import os
from urllib.parse import urlparse
from pathlib import Path
from playwright.sync_api import sync_playwright
URL=os.getenv('BIRTHDAY_URL','http://127.0.0.1:8765')
OUT=Path(os.getenv('BIRTHDAY_SCREENSHOTS','test-screenshots'));OUT.mkdir(parents=True,exist_ok=True)
MSG="Happy birthday jezneel!!!\nEven tho I got your number by accident (I swear, I thought you were my classmate jezneel tbh 😆), I'm glad you're part of my life, and I wish you all the very best as you venture into a new year...God bless you...keep growing, and never stop learning...keep in touch 😎\n-Caleb EJ"
def load(page):
 if os.getenv('BIRTHDAY_DIST')=='1':
  page.set_content((Path(__file__).resolve().parents[1]/'dist/index.html').read_text(),wait_until='domcontentloaded');return
 if os.getenv('BIRTHDAY_PREVIEW')=='1':
  page.set_content((Path(__file__).resolve().parents[1]/'preview.html').read_text(),wait_until='domcontentloaded');return
 if os.getenv('BIRTHDAY_INLINE')!='1':
  page.goto(URL,wait_until='domcontentloaded');return
 root=Path(__file__).resolve().parents[1]
 html=(root/'index.html').read_text(); css=(root/'src/style.css').read_text().split('\n',1)[1]
 art=(root/'src/art.js').read_text().replace('export function initArt','function initArt')
 main=(root/'src/main.js').read_text().replace("import {initArt} from './art.js';",'')
 html=html.replace('<link rel="stylesheet" href="./src/style.css"/>','<style>'+css+'</style>').replace('<script type="module" src="./src/main.js"></script>','<script type="module">'+art+'\n'+main+'</script>')
 page.set_content(html,wait_until='domcontentloaded')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox','--enable-unsafe-swiftshader'])
 for name,viewport,touch in [('desktop',{'width':1440,'height':900},False),('mobile-small',{'width':320,'height':568},True),('mobile',{'width':390,'height':844},True),('mobile-large',{'width':430,'height':932},True)]:
  if os.getenv('BIRTHDAY_ONLY') and name!=os.getenv('BIRTHDAY_ONLY'):continue
  page=b.new_page(viewport=viewport,is_mobile=touch,has_touch=touch,device_scale_factor=1);page.set_default_timeout(8000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.route('https://fonts.googleapis.com/**',lambda r:r.abort());load(page);page.wait_for_function("document.documentElement.dataset.renderer");page.wait_for_timeout(1500);page.screenshot(path=str(OUT/f'{name}-opening.png'),full_page=True);print(name,'renderer',page.locator('html').get_attribute('data-renderer'));assert os.getenv('BIRTHDAY_REQUIRE_THREE')!='1' or page.locator('html').get_attribute('data-renderer')=='three'
  def click(sel):
   loc=page.locator(sel);loc.tap() if touch else loc.click();page.wait_for_timeout(180)
   print(name,'tap',sel,page.locator('#sceneNo').inner_text(),flush=True)
  c=page.context.new_cdp_session(page) if touch else None
  def touchpath(points,hold=0):
   c.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':points[0][0],'y':points[0][1]}]})
   for x,y in points[1:]:c.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y}]})
   if hold:page.wait_for_timeout(hold)
   c.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
  click('#start');click('[data-color="2"]');assert page.locator('[data-color="2"]').get_attribute('aria-pressed')=='true';click('#next');assert page.locator('#next').is_disabled()
  for i in ['flour','sugar','butter','egg']:
   if i=='flour' and touch and os.getenv('BIRTHDAY_GESTURE')=='1' and viewport['height']>=800:
    r=page.locator('[data-ingredient=flour]').bounding_box();q=page.locator('#stage').bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']/2;tx=q['x']+q['width']/2;ty=q['y']+q['height']*.65;touchpath([(x+(tx-x)*j/15,y+(ty-y)*j/15) for j in range(16)]);assert page.locator('[data-ingredient=flour]').is_disabled()
   else:click('[data-ingredient="'+i+'"]')
   if i=='egg':page.wait_for_timeout(340);page.screenshot(path=str(OUT/f'{name}-egg.png'),full_page=True)
  page.wait_for_function("!document.getElementById('next').disabled");click('#next');page.wait_for_timeout(500);page.screenshot(path=str(OUT/f'{name}-mix.png'),full_page=True)
  if not touch:
   r=page.locator('#gesture').bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']*.65;page.mouse.move(x,y);page.mouse.down()
   import math
   for i in range(55):page.mouse.move(x+65*math.cos(i*.35),y+65*math.sin(i*.35))
   page.mouse.up()
  elif os.getenv('BIRTHDAY_GESTURE')=='1':
   import math
   page.locator('#gesture').scroll_into_view_if_needed();page.wait_for_timeout(200);r=page.locator('#gesture').bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']/2;touchpath([(x+45*math.cos(i*.35),y+45*math.sin(i*.35)) for i in range(100)])
  else:
   for i in range(4):click('#mixTap')
  assert page.locator('#next').is_enabled();click('#next');page.wait_for_timeout(450);page.screenshot(path=str(OUT/f'{name}-pour.png'),full_page=True);page.locator('#bake').wait_for();click('#bake');page.wait_for_function("document.getElementById('stage').dataset.oven==='open'");page.wait_for_timeout(180);page.screenshot(path=str(OUT/f'{name}-oven-open.png'),full_page=True);
  if touch and os.getenv('BIRTHDAY_GESTURE')=='1':
   page.locator('#gesture').scroll_into_view_if_needed();r=page.locator('#gesture').bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']*.8;touchpath([(x,y-r['height']*.45*j/10) for j in range(11)])
  else:click('#bake');
  page.wait_for_function("document.getElementById('stage').dataset.oven==='loaded'");click('#bake');page.wait_for_function("document.getElementById('stage').dataset.oven==='baking'");click('#bake');page.wait_for_timeout(2500);page.screenshot(path=str(OUT/f'{name}-oven-peek.png'),full_page=True);page.wait_for_function("document.getElementById('stage').dataset.oven==='done'");click('#bake');page.locator('#frostTap').wait_for(timeout=5000)
  if touch and os.getenv('BIRTHDAY_GESTURE')=='1':
   page.locator('#gesture').scroll_into_view_if_needed();page.wait_for_timeout(200);r=page.locator('#gesture').bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']/2;touchpath([(x+(-1)**i*70,y+(i%5)*5) for i in range(12)])
  else:
   for i in range(4):click('#frostTap')
  click('#next')
  if touch:
   for i in range(6):page.locator('#gesture').tap();page.wait_for_timeout(150)
  else:
   for i in range(6):click('#berryTap')
  assert page.locator('#next').is_enabled();click('#next');page.wait_for_timeout(600);page.screenshot(path=str(OUT/f'{name}-cake.png'),full_page=True);
  if touch and os.getenv('BIRTHDAY_GESTURE')=='1' and page.locator('html').get_attribute('data-renderer')=='illustrated':
   page.locator('#gesture').scroll_into_view_if_needed();points=page.evaluate('''()=>{let svg=document.querySelector('#art svg');return [[566,475],[450,283]].map(([x,y])=>{let p=svg.createSVGPoint();p.x=x;p.y=y;p=p.matrixTransform(svg.getScreenCTM());return [p.x,p.y]})}''');(x,y),(tx,ty)=points;touchpath([(x+(tx-x)*j/15,y+(ty-y)*j/15) for j in range(16)]);page.locator('#openLetter').wait_for()
  else:click('#light');
  page.wait_for_timeout(1100);page.screenshot(path=str(OUT/f'{name}-night.png'),full_page=True);click('#openLetter');page.wait_for_timeout(1100);assert 0<len(page.locator('#typed').inner_text())<len(MSG);click('#skipTyping');assert page.locator('#typed').inner_text()==MSG;page.screenshot(path=str(OUT/f'{name}-letter.png'),full_page=True);click('#letterDone');page.locator('#blow').scroll_into_view_if_needed();page.wait_for_timeout(450);r=page.locator('#blow').bounding_box();
  if touch and os.getenv('BIRTHDAY_GESTURE')=='1':touchpath([(r['x']+r['width']/2,r['y']+r['height']/2)],1600)
  elif touch:click('#blowAlt')
  else:page.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2);page.mouse.down();page.wait_for_timeout(1600);page.mouse.up()
  page.locator('#again').wait_for();page.wait_for_timeout(500);assert page.evaluate("Number(getComputedStyle(document.querySelector('#nightGlow')).opacity)<.1") if page.locator('html').get_attribute('data-renderer')=='illustrated' else True;page.screenshot(path=str(OUT/f'{name}-finale.png'),full_page=True);click('#readAgain');click('#skipTyping');assert page.locator('#typed').inner_text()==MSG;click('#letterDone');click('#again');page.locator('#start').wait_for();assert not errors,errors;assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1');print(name,'PASS: full sequence, exact letter, replay, no page errors');page.close()
 b.close()
