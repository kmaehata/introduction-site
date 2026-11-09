// 公開用の資料を書き出す。使い方: node export.js <slides dir> <out dir>
// 冊子ごとに 01.jpg… と <deck>.pdf、全体の目次 manifest.json を作る。
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [dir, out] = process.argv.slice(2);

const decks = {
  architecture: ['cover-arch', 'arch', 'archeng', 'archaws'],
  flow: ['cover-flow', 'team', 'split', 'day', 'flow', 'flowplan', 'flowtrade'],
  business: ['cover-biz', 'oneline', 'aim', 'books', 'safety', 'slack', 'webtop', 'webao', 'webtabs', 'measure', 'stage'],
};

// アイコン(線画、24x24)
const I = {
  Settings: '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
  Search: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>',
  Lightbulb: '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
  CheckCircle: '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
  Check: '<path d="M20 6 9 17l-5-5"/>',
  Book: '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>',
  Chat: '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
  Users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
  Chart: '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
  Verified: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/>',
  Trust: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>',
  Globe: '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
  Lock: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
  Key: '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6"/><path d="m15.5 7.5 3 3L22 7l-3-3"/>',
  Clock: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
  Lightning: '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
  Activity: '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
  Wrench: '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
  Play: '<path d="m6 3 14 9-14 9V3z"/>',
  Star: '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
  Database: '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/>',
  Cloud: '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>',
  PaperPlane: '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
  Home: '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
  Warning: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
  Link: '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
};

const css = `
*{margin:0;padding:0;box-sizing:border-box}
@page{size:1920px 1080px;margin:0}
body{background:#fff}
section{position:relative;width:1920px;height:1080px;overflow:hidden;break-after:page}
p{font-size:32px;line-height:1.4} h1{font-size:96px} h2{font-size:64px} h3{font-size:44px}
h1,h2,h3{line-height:1.15}
aside{display:none}
div{display:flex;flex-direction:column}
x-icon{display:inline-flex;flex:none}
x-icon svg{width:100%;height:100%}
x-shape{display:block;flex:none;clip-path:polygon(0 28%,60% 28%,60% 0,100% 50%,60% 100%,60% 72%,0 72%)}
table{border-collapse:collapse} th,td{border-bottom:2px solid #E2DED3;padding:10px 16px;text-align:left}
th{font-weight:700}
`;

const head = `<meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700&family=Noto+Sans+JP:wght@400;500;700&display=swap"><style>${css}</style>`;
const fixIcons = (icons) => {
  document.querySelectorAll('x-icon').forEach((e) => {
    const body = icons[e.getAttribute('name')];
    if (!body) throw new Error('unknown icon ' + e.getAttribute('name'));
    e.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${body}</svg>`;
  });
};
const titleOf = (html) => {
  const m = html.match(/<h2[^>]*>([\s\S]*?)<\/h2>/) || html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/);
  return m ? m[1].replace(/<[^>]+>/g, '').trim() : '';
};

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const manifest = {};
  for (const [deck, ids] of Object.entries(decks)) {
    const ddir = path.join(out, deck);
    fs.rmSync(ddir, { recursive: true, force: true });
    fs.mkdirSync(ddir, { recursive: true });
    const htmls = ids.map((id) => fs.readFileSync(path.join(dir, id + '.html'), 'utf8'));
    manifest[deck] = ids.map((id, i) => ({ file: `${String(i + 1).padStart(2, '0')}.jpg`, title: titleOf(htmls[i]) }));
    for (let i = 0; i < ids.length; i++) {
      await p.setContent(`<!doctype html><html><head>${head}</head><body>${htmls[i]}</body></html>`, { waitUntil: 'networkidle' });
      await p.evaluate(fixIcons, I);
      await p.evaluate(() => document.fonts.ready);
      await p.screenshot({ path: path.join(ddir, manifest[deck][i].file), type: 'jpeg', quality: 82 });
    }
    await p.setContent(`<!doctype html><html><head>${head}</head><body>${htmls.join('\n')}</body></html>`, { waitUntil: 'networkidle' });
    await p.evaluate(fixIcons, I);
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.join(out, `${deck}.pdf`), width: '1920px', height: '1080px', printBackground: true });
    console.log(deck, ids.length, 'slides');
  }
  fs.writeFileSync(path.join(out, 'manifest.json'), JSON.stringify(manifest, null, 2));
  await b.close();
})();
