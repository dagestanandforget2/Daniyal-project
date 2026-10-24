"""shot.py PROJECT_DIR t1 t2 ...  -> PROJECT_DIR/chk.jpg (stills side by side, half size). Prints page errors."""
import asyncio, sys, os
from playwright.async_api import async_playwright
from PIL import Image
d=os.path.abspath(sys.argv[1]); ts=[float(x) for x in sys.argv[2:]]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':540,'height':960})
        pg.on('pageerror',lambda e:print('ERR',e))
        await pg.goto('file://'+d+'/film.html'); await pg.wait_for_timeout(1200)
        ims=[]
        for t in ts:
            await pg.evaluate(f"window.__seek({t})")
            await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))"); await pg.wait_for_timeout(60)
            await pg.screenshot(path=d+'/_k.png'); ims.append(Image.open(d+'/_k.png').convert('RGB').resize((270,480)))
        await b.close()
    S=Image.new('RGB',(270*len(ims),480))
    for i,im in enumerate(ims): S.paste(im,(i*270,0))
    S.save(d+'/chk.jpg',quality=85)
asyncio.run(main())
