// Frame-by-frame renderer: calls seek(t) in headless Chromium, screenshots, pipes frames to ffmpeg.
// Stills:   node tools/render.mjs --still 1,5.5,12 --scale 1 --out out/stills
// Video:    node tools/render.mjs --scale 0.5 --workers 4 --out out/preview_silent.mp4 [--from 0 --to 57]
//   --scale = deviceScaleFactor (2 = full quality, supersampled down to 1080x1920; 0.5 = fast preview 540x960)
import { createRequire } from 'module';
import { spawn } from 'child_process';
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const require = createRequire(import.meta.url);
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i < 0 ? d : process.argv[i + 1]; };
const scale = parseFloat(arg('scale', '1')), workers = parseInt(arg('workers', '4')), fps = 30;
const out = arg('out', 'out/render.mp4'), still = arg('still', null);
const from = parseFloat(arg('from', '0')), to = parseFloat(arg('to', '57'));
const url = 'file://' + path.join(root, 'src/index.html');
const exe = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

async function open(browser) {
  const ctx = await browser.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: scale });
  const page = await ctx.newPage();
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto(url); await page.evaluate(() => window.READY);
  return page;
}
const launch = () => chromium.launch({ executablePath: fs.existsSync(exe) ? exe : undefined, args: ['--no-sandbox', '--font-render-hinting=none', '--disable-gpu'] });

if (still) {
  fs.mkdirSync(path.join(root, out), { recursive: true });
  const b = await launch(); const page = await open(b);
  for (const t of still.split(',').map(Number)) {
    await page.evaluate(t => window.seek(t), t);
    await page.screenshot({ path: path.join(root, out, `t${t.toFixed(2).padStart(6, '0')}.png`) });
    console.log('still', t);
  }
  await b.close(); process.exit(0);
}

const N0 = Math.round(from * fps), N1 = Math.round(to * fps);
const chunk = Math.ceil((N1 - N0) / workers);
const tmp = path.join(root, 'out/chunks'); fs.mkdirSync(tmp, { recursive: true });
const jobs = [];
for (let w = 0; w < workers; w++) {
  const a = N0 + w * chunk, bnd = Math.min(N1, a + chunk); if (a >= bnd) continue;
  jobs.push((async () => {
    const f = path.join(tmp, `c${w}.mp4`);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
      '-vf', 'scale=1080:1920:flags=lanczos', '-c:v', 'libx264', '-preset', 'fast', '-crf', scale >= 1 ? '12' : '20', '-pix_fmt', 'yuv420p', f]);
    ff.stderr.on('data', d => process.stderr.write(d));
    const done = new Promise(r => ff.on('close', r));
    const b = await launch(); const page = await open(b);
    for (let n = a; n < bnd; n++) {
      await page.evaluate(t => window.seek(t), n / fps);
      const buf = await page.screenshot({ type: 'jpeg', quality: 96 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (n % 60 === 0) console.log(`w${w} frame ${n}/${bnd}`);
    }
    ff.stdin.end(); await done; await b.close(); return f;
  })());
}
const files = await Promise.all(jobs);
fs.writeFileSync(path.join(tmp, 'list.txt'), files.map(f => `file '${f}'`).join('\n'));
await new Promise(r => spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'list.txt'), '-c', 'copy', path.join(root, out)]).on('close', r));
console.log('wrote', out);
