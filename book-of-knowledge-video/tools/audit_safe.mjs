import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
const p = await (await b.newContext({ viewport: { width: 1080, height: 1920 } })).newPage();
await p.goto('file:///home/user/Daniyal-project/book-of-knowledge-video/src/index.html'); await p.evaluate(() => window.READY);
const seen = new Set();
for (let t = 0; t < 57; t += 0.25) { const bad = await p.evaluate(t => window.auditSafe(t), t); bad.forEach(x => { const k = JSON.stringify(x); if (!seen.has(k)) { seen.add(k); console.log(t, k); } }); }
console.log('audit done'); await b.close();
