"""render.py PROJECT_DIR START_FRAME END_FRAME OUT.mp4   (30 fps, 1080x1920)"""
import asyncio, subprocess, sys, os
from playwright.async_api import async_playwright
FPS=30; d=os.path.abspath(sys.argv[1]); a,b,out=int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
async def main():
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-',
        '-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium',out],stdin=subprocess.PIPE)
    async with async_playwright() as p:
        br=await p.chromium.launch()
        pg=await br.new_page(viewport={'width':540,'height':960},device_scale_factor=2)
        await pg.goto('file://'+d+'/film.html'); await pg.wait_for_timeout(2000)
        for i in range(a,b):
            await pg.evaluate(f"window.__seek({i/FPS})")
            await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
            ff.stdin.write(await pg.screenshot(type='jpeg',quality=93))
            if i%50==0: print(i,flush=True)
        await br.close()
    ff.stdin.close(); ff.wait(); print('DONE',flush=True)
asyncio.run(main())
