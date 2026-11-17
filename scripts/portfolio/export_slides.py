# introduction-site の scripts/portfolio/export-slides.js と同じ見た目で、スライドを JPEG と PDF に書き出す。
# 使い方: python export_slides.py <export-slides.js> <スライドのフォルダ> <出力先> <冊子名>
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

js_path, src, out, deck = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
js = js_path.read_text(encoding="utf-8")
css = re.search(r"const css = `([\s\S]*?)`;", js).group(1)
head_tpl = re.search(r"const head = `([\s\S]*?)`;", js).group(1)
head = head_tpl.replace("${css}", css)
icons = dict(re.findall(r"^\s*(\w+): '(.*)',$", js, re.M))
# v1.1 で足したアイコン(同じ線画の形式)
icons.update({
    "ArrowDown": '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
    "Bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "Shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>',
})
order = (src / "order.txt").read_text(encoding="utf-8").split()
htmls = [(src / f"{sid}.html").read_text(encoding="utf-8") for sid in order]


def title_of(html):
    m = re.search(r"<h2[^>]*>([\s\S]*?)</h2>", html) or re.search(r"<h1[^>]*>([\s\S]*?)</h1>", html)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""


FIX = """(icons) => { document.querySelectorAll('x-icon').forEach((e) => {
  const body = icons[e.getAttribute('name')];
  if (!body) throw new Error('unknown icon ' + e.getAttribute('name'));
  e.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${body}</svg>`;
}); }"""

ddir = out / deck
ddir.mkdir(parents=True, exist_ok=True)
for f in ddir.glob("*.jpg"):
    f.unlink()
manifest = {deck: [{"file": f"{i + 1:02d}.jpg", "title": title_of(h)} for i, h in enumerate(htmls)]}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    for i, h in enumerate(htmls):
        pg.set_content(f"<!doctype html><html><head>{head}</head><body>{h}</body></html>", wait_until="networkidle")
        pg.evaluate(FIX, icons)
        pg.evaluate("() => document.fonts.ready")
        pg.screenshot(path=str(ddir / manifest[deck][i]["file"]), type="jpeg", quality=82)
    pg.set_content(f"<!doctype html><html><head>{head}</head><body>{''.join(htmls)}</body></html>", wait_until="networkidle")
    pg.evaluate(FIX, icons)
    pg.evaluate("() => document.fonts.ready")
    pg.pdf(path=str(out / f"{deck}.pdf"), width="1920px", height="1080px", print_background=True)
    b.close()
(out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(deck, len(htmls), "slides")
