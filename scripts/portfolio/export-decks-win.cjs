// WSL から Windows の Node.js と Chrome を使って、スライドを JPEG と PDF に書き出す。
// export-slides.js と同じ CSS・フォント・アイコンを読み込むので、見た目は同じになる。
//
// 使い方(Windows の Node で実行。playwright-core は作業フォルダに入れておく):
//   node.exe export-decks-win.cjs <export-slides.js> <スライドのフォルダ> <出力先>
// スライドのフォルダの decks.json({"冊子名": ["スライドID", ...]})の順で冊子を作る。
const fs = require('fs');
const path = require('path');
const { chromium } = require(require.resolve('playwright-core', { paths: [process.cwd()] }));

const [jsPath, src, out] = process.argv.slice(2);
const js = fs.readFileSync(jsPath, 'utf8');
const css = js.match(/const css = `([\s\S]*?)`;/)[1];
const head = js.match(/const head = `([\s\S]*?)`;/)[1].replace('${css}', css);
const icons = Object.fromEntries([...js.matchAll(/^\s*(\w+): '(.*)',$/gm)].map((m) => [m[1], m[2]]));
// 追加のアイコン(同じ線画の形式)
Object.assign(icons, {
  ArrowDown: '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
  Bell: '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
  Shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>',
});
const decks = JSON.parse(fs.readFileSync(path.join(src, 'decks.json'), 'utf8'));

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
  const b = await chromium.launch({
    executablePath: process.env.CHROME || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const manifest = {};
  for (const [deck, ids] of Object.entries(decks)) {
    const ddir = path.join(out, deck);
    fs.rmSync(ddir, { recursive: true, force: true });
    fs.mkdirSync(ddir, { recursive: true });
    const htmls = ids.map((id) => fs.readFileSync(path.join(src, id + '.html'), 'utf8'));
    manifest[deck] = ids.map((id, i) => ({ file: `${String(i + 1).padStart(2, '0')}.jpg`, title: titleOf(htmls[i]) }));
    for (let i = 0; i < ids.length; i++) {
      await p.setContent(`<!doctype html><html><head>${head}</head><body>${htmls[i]}</body></html>`, { waitUntil: 'networkidle' });
      await p.evaluate(fixIcons, icons);
      await p.evaluate(() => document.fonts.ready);
      await p.screenshot({ path: path.join(ddir, manifest[deck][i].file), type: 'jpeg', quality: 82 });
    }
    await p.setContent(`<!doctype html><html><head>${head}</head><body>${htmls.join('')}</body></html>`, { waitUntil: 'networkidle' });
    await p.evaluate(fixIcons, icons);
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.join(out, `${deck}.pdf`), width: '1920px', height: '1080px', printBackground: true });
    console.log(deck, ids.length, 'slides');
  }
  fs.writeFileSync(path.join(out, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
  await b.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
