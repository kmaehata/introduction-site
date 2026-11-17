# v1.1 の変更点の資料(スライド HTML)を作る。使い方: python make_slides.py <出力フォルダ> <demo-top.png のあるフォルダ>
# 見た目は v1.0 の資料(introduction-site の scripts/portfolio)に合わせる。図はすべて SVG。
import base64
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

NAVY, INK, SUB, BG, CARD, LINE = "#16213A", "#1B2440", "#5B6478", "#F4F2EE", "#FDFCF8", "#E2DED3"
MID, GUARD, ATTACK, ACCENT, BLUE, RED, GREEN = "#6B4FBB", "#138A7A", "#E07B2F", "#C8641E", "#2A78D6", "#D2433B", "#1E8E5A"
MID_S, GUARD_S, ATTACK_S, PANEL = "#E9E4F7", "#DCF1EC", "#FBE6D5", "#E9EEF6"
HEAD = "font-family:'Zen Maru Gothic','Noto Sans JP',sans-serif;font-weight:700"
BODY = "font-family:'Noto Sans JP',sans-serif"


def page(sid, eyebrow, title, inner, bg=BG):
    return (f'<section id="{sid}" style="background:{bg};color:{INK};{BODY};padding:110px 128px 80px;'
            f'display:flex;flex-direction:column;gap:44px">'
            f'<div style="gap:14px"><p style="font-size:26px;font-weight:700;color:{ACCENT}">{eyebrow}</p>'
            f'<h2 style="{HEAD};font-size:64px;color:{INK}">{title}</h2></div>{inner}</section>')


def row(*children, gap=32, align="stretch", style=""):
    return f'<div style="display:flex;flex-direction:row;gap:{gap}px;align-items:{align};{style}">{"".join(children)}</div>'


def card(inner, top=None, bg=CARD, style=""):
    border = f"border-top:14px solid {top};" if top else ""
    return (f'<div style="flex:1;background:{bg};border:2px solid {LINE};{border}border-radius:28px;padding:34px 38px;'
            f'gap:18px;{style}">{inner}</div>')


def pill(text, fg, bg, size=26):
    return f'<p style="font-size:{size}px;font-weight:700;color:{fg};background:{bg};padding:6px 22px;border-radius:999px">{text}</p>'


def icon(name, color, size=40):
    return f'<x-icon name="{name}" style="width:{size}px;height:{size}px;color:{color}"></x-icon>'


def img(path, style):
    data = base64.b64encode(Path(path).read_bytes()).decode()
    return f'<img src="data:image/png;base64,{data}" style="{style}">'


slides = {}

# ---------------------------------------------------------------- 表紙
toc = ["ひとことで言うと", "v1.0 の11日間で起きたこと", "なぜ損切りばかりだったのか", "デイ攻めの新しいルール",
       "デイ守りの新しいルール", "過去の値動きで確かめる", "ミドルは「知らせる係」に", "比べる相手を増やし、100万円から再スタート",
       "Webアプリ:ログインなしで見られるデモ", "これから測ること"]
items = "".join(
    f'<div style="display:flex;flex-direction:row;align-items:center;gap:20px;border-bottom:1px solid #2E3D63;padding:9px 0px">'
    f'<p style="width:56px;font-size:24px;font-weight:700;color:#F2B27A">{i + 1:02d}</p>'
    f'<p style="font-size:28px;color:#E6EBF5">{t}</p></div>' for i, t in enumerate(toc))
slides["cover"] = (
    f'<section id="cover" style="background:{NAVY};color:#F6F4EE;{BODY};padding:100px 128px;display:flex;flex-direction:row;align-items:center;gap:96px">'
    f'<div style="width:780px;gap:28px"><p style="font-size:28px;font-weight:700;letter-spacing:2px;color:#F2B27A">AIトレードデスク ・ Version 1.1</p>'
    f'<p style="{HEAD};font-size:120px;line-height:1;color:#3A4A6B">04</p>'
    f'<h1 style="{HEAD};font-size:84px;line-height:1.2">v1.1 の変更点</h1>'
    f'<p style="font-size:36px;line-height:1.5;color:#C9D3E6">負け方を調べて、ルールを作り直した</p>'
    f'{row(pill("エンジニア・ビジネス", NAVY, "#F2B27A"), gap=12)}</div>'
    f'<div style="flex:1;gap:2px"><p style="font-size:24px;font-weight:700;letter-spacing:4px;color:#8A96AD;padding:0 0 10px">CONTENTS</p>{items}</div></section>')


# ---------------------------------------------------------------- 01 ひとことで
def change(name, color, soft, before, after, ic):
    return card(
        row(f'<h3 style="{HEAD};font-size:44px">{name}</h3>', gap=12, align="center") +
        f'<div style="background:#F1EEE6;border-radius:18px;padding:18px 22px;gap:6px"><p style="font-size:22px;color:{SUB}">v1.0</p>'
        f'<p style="font-size:30px;color:{SUB}">{before}</p></div>'
        f'<div style="align-items:center">{icon("ArrowDown", color, 44)}</div>'
        f'<div style="background:{soft};border-radius:18px;padding:18px 22px;gap:6px"><p style="font-size:22px;font-weight:700;color:{color}">v1.1</p>'
        f'<p style="font-size:30px;font-weight:700">{after}</p></div>', top=color)


slides["oneline"] = page("oneline", "ひとことで言うと", "負け方を調べて、3つの財布の役割を作り直した", row(
    change("ミドル", MID, MID_S, "自動で売買<br>(下落相場で取引0回)", "売買はせず<br>買い時を Slack で知らせる", "Bell"),
    change("デイ守り", GUARD, GUARD_S, "条件が厳しく<br>取引0回", "1日2〜3回<br>小さく取引する", "Shield"),
    change("デイ攻め", ATTACK, ATTACK_S, "15分足の突破<br>54回中38回が損切り", "1時間足の押し・戻り<br>損失を大きく縮小", "Lightning"),
))

# ---------------------------------------------------------------- 02 v1.0 の11日間


def hbar(label, value, color, max_abs=20, note=""):
    w = abs(value) / max_abs * 540
    zero = "#B9B4A8"
    bar = (f'<div style="width:540px;height:46px;position:relative;background:#EFECE4;border-radius:10px">'
           f'<div style="position:absolute;right:0;top:0;height:46px;width:{w}px;background:{color};border-radius:10px"></div></div>'
           if value < 0 else
           f'<div style="width:540px;height:46px;background:#EFECE4;border-radius:10px;justify-content:center;padding-left:24px">'
           f'<p style="font-size:24px;color:{SUB}">{note}</p></div>')
    val = f'<p style="width:170px;font-size:34px;font-weight:700;color:{RED if value < 0 else SUB}">{value:+.1f}%</p>' if value else \
        f'<p style="width:170px;font-size:34px;font-weight:700;color:{SUB}">0%</p>'
    return row(f'<p style="width:360px;font-size:30px;font-weight:500">{label}</p>', bar, val, gap=24, align="center")


donut_r, donut_c = 120, 2 * 3.14159 * 120
stop_share = 38 / 54
donut = (f'<svg width="320" height="320" viewBox="0 0 320 320"><circle cx="160" cy="160" r="{donut_r}" fill="none" stroke="#EFECE4" stroke-width="56"/>'
         f'<circle cx="160" cy="160" r="{donut_r}" fill="none" stroke="{RED}" stroke-width="56" stroke-dasharray="{donut_c * stop_share} {donut_c}" transform="rotate(-90 160 160)"/>'
         f'<text x="160" y="150" text-anchor="middle" font-size="64" font-weight="700" fill="{INK}" font-family="Noto Sans JP">38</text>'
         f'<text x="160" y="200" text-anchor="middle" font-size="28" fill="{SUB}" font-family="Noto Sans JP">/ 54回</text></svg>')
slides["v10"] = page("v10", "v1.0 の11日間(11/6〜11/17)", "強い下落相場で、守りは動けず、攻めは損切りが続いた", row(
    card(f'<p style="font-size:28px;font-weight:700;color:{SUB}">期間中の損益(各100万円から)</p>' +
         hbar("買って持ち続ける(比較)", -15.8, "#8A6FD1") + hbar("デイ攻め(ルールのみ)", -17.1, "#E9A774") +
         hbar("デイ攻め(AI あり)", -12.1, ATTACK) + hbar("デイ守り", 0, GUARD, note="取引 0回") +
         hbar("ミドル", 0, MID, note="取引 0回"), style="flex:none;width:1200px;gap:26px"),
    card(f'<p style="font-size:28px;font-weight:700;color:{SUB}">デイ攻めの決済のうち損切り</p>'
         f'<div style="align-items:center">{donut}</div>'
         f'<p style="font-size:28px;line-height:1.5">入って<b>平均20分</b>ほどで損切りに掛かっていた</p>', style="gap:20px"),
    gap=36))

# ---------------------------------------------------------------- 03 なぜ損切りばかり


def ruler(stop, label, color, verdict, good, noise_pct=0.30, noise_label="15分足のふつうの揺れ 約0.3%"):
    scale = 900  # 1% = 900px
    cost = 0.12 * scale
    noise = noise_pct * scale
    return (f'<div style="gap:14px"><p style="font-size:30px;font-weight:700">{label}</p>'
            f'<svg width="1100" height="175" viewBox="0 0 1100 175">'
            f'<rect x="0" y="40" width="{noise}" height="56" rx="8" fill="#E6E2D8"/>'
            f'<text x="12" y="76" font-size="22" fill="{SUB}" font-family="Noto Sans JP">{noise_label}</text>'
            f'<rect x="0" y="100" width="{cost}" height="30" rx="6" fill="#B9B4A8"/>'
            f'<text x="0" y="168" font-size="20" fill="{SUB}" font-family="Noto Sans JP">売買コスト(往復)約0.1%</text>'
            f'<line x1="{stop * scale}" y1="10" x2="{stop * scale}" y2="140" stroke="{color}" stroke-width="6"/>'
            f'<text x="{stop * scale + 14}" y="34" font-size="26" font-weight="700" fill="{color}" font-family="Noto Sans JP">損切り {stop}%</text></svg>'
            f'{row(icon("CheckCircle" if good else "Warning", GREEN if good else RED, 34), f"<p style=font-size:28px>{verdict}</p>", gap=12, align="center")}</div>')


slides["why"] = page("why", "原因の調査", "損切りの幅が、ふつうの揺れとほぼ同じだった", row(
    card(ruler(0.36, "v1.0 デイ攻め(15分足)", RED, "ふつうの揺れだけで損切りに届く。コストも損切り幅の3割", False) +
         '<div style="height:12px"></div>' +
         ruler(1.0, "v1.1 デイ攻め(1時間足)", GREEN, "損切りは揺れの1.5倍。コストの重さは約1割に", True, 0.67, "1時間足のふつうの揺れ 約0.7%"), style="flex:2.3;gap:20px"),
    card(f'{icon("Search", BLUE, 52)}<p style="font-size:30px;font-weight:700">損切りのあと、元の利確価格まで届いたのは</p>'
         f'<p style="{HEAD};font-size:96px;color:{INK}">7<span style="font-size:44px;color:{SUB}"> / 30件</span></p>'
         f'<p style="font-size:28px;line-height:1.5;color:{SUB}">幅を広げるだけでは救えない。<br><b style="color:{INK}">時間軸そのものを上げる</b>ことにした</p>',
         bg=PANEL, style="border:none;gap:18px"),
    gap=36))

# ---------------------------------------------------------------- 04 デイ攻め


def trend_chart(sign, color, width=900, height=470):
    # 上昇の流れ(破線)の中で、1時間足が20本平均(青)まで押してから上に戻したところで入る
    price = [(40, 400), (90, 360), (140, 375), (190, 320), (240, 300), (290, 315), (340, 260), (390, 235),
             (440, 255), (490, 200), (540, 180), (590, 200), (630, 235), (665, 250), (700, 225)]
    sma = [(40, 430), (140, 395), (240, 345), (340, 300), (440, 270), (540, 235), (665, 250), (760, 215)]
    path = " ".join(f"{'M' if i == 0 else 'L'}{x},{y}" for i, (x, y) in enumerate(price))
    spath = " ".join(f"{'M' if i == 0 else 'L'}{x},{y}" for i, (x, y) in enumerate(sma))
    ex, ey = price[-1]
    stop_y, tp_y = 300, 80
    t = 'font-family="Noto Sans JP"'
    return (f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
            f'<line x1="40" y1="440" x2="820" y2="120" stroke="#B9B4A8" stroke-width="4" stroke-dasharray="14 12"/>'
            f'<text x="60" y="455" font-size="24" fill="{SUB}" {t}>4時間足の流れ(上向き)</text>'
            f'<path d="{spath}" fill="none" stroke="{BLUE}" stroke-width="5" opacity="0.75"/>'
            f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<ellipse cx="660" cy="248" rx="46" ry="26" fill="none" stroke="{BLUE}" stroke-width="3"/>'
            f'<text x="470" y="300" font-size="22" fill="{BLUE}" {t}>平均まで押した</text>'
            f'<line x1="690" y1="{stop_y}" x2="880" y2="{stop_y}" stroke="{RED}" stroke-width="4" stroke-dasharray="10 8"/>'
            f'<text x="880" y="{stop_y + 32}" text-anchor="end" font-size="22" font-weight="700" fill="{RED}" {t}>損切り(揺れ×1.5)</text>'
            f'<line x1="690" y1="{tp_y}" x2="880" y2="{tp_y}" stroke="{GREEN}" stroke-width="4" stroke-dasharray="10 8"/>'
            f'<text x="880" y="{tp_y - 14}" text-anchor="end" font-size="22" font-weight="700" fill="{GREEN}" {t}>利確(損切りの2倍)</text>'
            f'<line x1="{ex}" y1="{ey}" x2="{ex}" y2="{tp_y + 12}" stroke="{GREEN}" stroke-width="3" opacity="0.5"/>'
            f'<line x1="{ex}" y1="{ey}" x2="{ex}" y2="{stop_y - 12}" stroke="{RED}" stroke-width="3" opacity="0.5"/>'
            f'<circle cx="{ex}" cy="{ey}" r="18" fill="{color}" stroke="#fff" stroke-width="5"/>'
            f'<text x="{ex + 30}" y="{ey + 9}" font-size="26" font-weight="700" fill="{color}" {t}>ここで入る</text>'
            f'<text x="60" y="40" font-size="22" fill="{BLUE}" {t}>青: 1時間足の20本平均 ・ 売りはこの逆さま</text></svg>')


steps = "".join(
    row(f'<p style="{HEAD};width:64px;height:64px;border-radius:999px;background:{ATTACK};color:#fff;font-size:34px;align-items:center;justify-content:center;display:flex">{n}</p>',
        f'<p style="flex:1;font-size:30px;line-height:1.45">{t}</p>', gap=20, align="center")
    for n, t in ((1, "4時間足で<b>流れの向き</b>を決める(上なら買い、下なら売り)"),
                 (2, "1時間足が<b>20本平均まで押す(戻す)</b>のを待つ"),
                 (3, "流れの方向の足で引けたら入る。<b>RSI が行き過ぎていない</b>ときだけ"),
                 (4, "1回のリスクは資金の <b>3% → 0.5%</b>")))
slides["attack"] = page("attack", "デイ攻め ・ 新しいルール", "流れに逆らわず、押し目と戻りで入る", row(
    card(trend_chart(1, ATTACK), style="flex:1.45;padding:20px 24px;align-items:center"),
    card(steps + row(pill("買いも売りも", ATTACK, ATTACK_S), pill("最大2倍", ATTACK, ATTACK_S), gap=12), top=ATTACK, style="gap:26px"),
    gap=32))

# ---------------------------------------------------------------- 05 デイ守り


def band_chart(width=760, height=400):
    import math
    mid = 170
    xs = [30 + i * 26 for i in range(27)]
    ys = [mid + 14 * math.sin(i / 1.3) for i in range(18)] + [mid + 25, mid + 65, mid + 110, mid + 150, mid + 170, mid + 160, mid + 135, mid + 122, mid + 115]
    price = " ".join(f"{'M' if i == 0 else 'L'}{x},{y:.0f}" for i, (x, y) in enumerate(zip(xs, ys)))
    upper = " ".join(f"{'M' if i == 0 else 'L'}{x},{mid - 60 - (0 if i < 18 else (i - 17) * 6):.0f}" for i, x in enumerate(xs))
    lower = " ".join(f"{'M' if i == 0 else 'L'}{x},{mid + 60 + (0 if i < 18 else (i - 17) * 7):.0f}" for i, x in enumerate(xs))
    ex, ey = xs[24], ys[24]
    return (f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
            f'<path d="{upper}" fill="none" stroke="#B9B4A8" stroke-width="3" stroke-dasharray="8 8"/>'
            f'<path d="{lower}" fill="none" stroke="{GUARD}" stroke-width="4" stroke-dasharray="10 8"/>'
            f'<text x="34" y="{mid + 96}" font-size="22" fill="{GUARD}" font-family="Noto Sans JP">ふだんの下限(−2σ)</text>'
            f'<path d="{price}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<text x="{xs[22]}" y="{ys[22] + 46}" font-size="24" font-weight="700" fill="{RED}" font-family="Noto Sans JP" text-anchor="middle">売られすぎ</text>'
            f'<circle cx="{ex}" cy="{ey}" r="16" fill="{GUARD}" stroke="#fff" stroke-width="5"/>'
            f'<text x="{ex + 10}" y="{ey - 75}" font-size="26" font-weight="700" fill="{GUARD}" font-family="Noto Sans JP" text-anchor="middle">戻したら買う</text></svg>')


def pull_chart(width=760, height=400):
    import math
    xs = [30 + i * 26 for i in range(27)]
    ys = [330 - i * 9 - 30 * math.sin(i / 2.0) for i in range(27)]
    ys[-4:] = [ys[-5] + 25, ys[-5] + 45, ys[-5] + 38, ys[-5] + 10]
    price = " ".join(f"{'M' if i == 0 else 'L'}{x},{y:.0f}" for i, (x, y) in enumerate(zip(xs, ys)))
    sma = " ".join(f"{'M' if i == 0 else 'L'}{x},{y + 40:.0f}" for i, (x, y) in enumerate(zip(xs[::3], ys[::3])))
    ex, ey = xs[-1], ys[-1]
    return (f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
            f'<path d="{sma}" fill="none" stroke="{BLUE}" stroke-width="4" opacity="0.7"/>'
            f'<path d="{price}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<circle cx="{ex}" cy="{ey}" r="16" fill="{GUARD}" stroke="#fff" stroke-width="5"/>'
            f'<text x="{ex - 30}" y="{ey - 34}" font-size="26" font-weight="700" fill="{GUARD}" font-family="Noto Sans JP" text-anchor="end">押したら買う</text>'
            f'<text x="34" y="390" font-size="22" fill="{BLUE}" font-family="Noto Sans JP">青: 15分足の20本平均</text></svg>')


slides["guard"] = page("guard", "デイ守り ・ 新しいルール", "下げの相場でも、小さく・こまめに取引する", row(
    card(f'<p style="font-size:30px;font-weight:700">A. 上げの相場の押し目</p>{pull_chart()}'
         f'<p style="font-size:26px;color:{SUB}">条件を「平均が上向き」に緩め、出番を増やした</p>', top=GUARD, style="align-items:flex-start"),
    card(f'<p style="font-size:30px;font-weight:700">B. 急落の行き過ぎからの戻り <span style="color:{GUARD}">NEW</span></p>{band_chart()}'
         f'<p style="font-size:26px;color:{SUB}">利確は損切りと同じ幅。小さく取って早く降りる</p>', top=GUARD, style="align-items:flex-start"),
    gap=32) + row(
    f'<div style="flex:1;background:{GUARD_S};border-radius:20px;padding:18px 28px;flex-direction:row;gap:16px;align-items:center">{icon("Shield", GUARD, 38)}'
    f'<p style="font-size:28px">1回のリスクは資金の <b>0.75% → 0.2%</b>。1日の損失の上限も <b>2% → 1.5%</b></p></div>'))

# ---------------------------------------------------------------- 06 バックテスト


def vbars(title, color, pairs, ymin=-70):
    # pairs: [(期間, v1, v2)]
    h, w0 = 330, 112
    svg = [f'<svg width="500" height="{h + 150}" viewBox="0 0 500 {h + 150}">',
           f'<line x1="20" y1="20" x2="490" y2="20" stroke="#B9B4A8" stroke-width="3"/>',
           f'<text x="44" y="14" font-size="20" fill="{SUB}" font-family="Noto Sans JP">0%</text>']
    for gi, (label, a, b) in enumerate(pairs):
        gx = 30 + gi * 240
        for k, (v, c, name) in enumerate(((a, "#C9C4B8", "v1.0"), (b, color, "v1.1"))):
            bh = abs(v) / abs(ymin) * h
            x = gx + k * (w0 - 20)
            svg.append(f'<rect x="{x}" y="20" width="{w0 - 40}" height="{bh:.0f}" rx="8" fill="{c}"/>')
            svg.append(f'<text x="{x + (w0 - 40) / 2}" y="{20 + bh + 34:.0f}" text-anchor="middle" font-size="28" font-weight="700" fill="{INK}" font-family="Noto Sans JP">{v:+.1f}%</text>')
            svg.append(f'<text x="{x + (w0 - 40) / 2}" y="{20 + bh + 64:.0f}" text-anchor="middle" font-size="20" fill="{SUB}" font-family="Noto Sans JP">{name}</text>')
        svg.append(f'<text x="{gx + 95}" y="{h + 140}" text-anchor="middle" font-size="24" font-weight="700" fill="{INK}" font-family="Noto Sans JP">{label}</text>')
    svg.append('</svg>')
    return card(f'<p style="{HEAD};font-size:38px;color:{color}">{title}</p>' + "".join(svg), top=color, style="align-items:center;gap:6px")


slides["backtest"] = page("backtest", "過去の値動きで確かめる(120日・AIなし・コスト込み)", "損失を大きく減らした。ただし、まだプラスではない", row(
    vbars("デイ攻め", ATTACK, [("選ぶのに使った80日", -36.4, -11.1), ("確かめた40日", -23.6, -2.3)]),
    vbars("デイ守り", GUARD, [("選ぶのに使った80日", -65.7, -16.7), ("確かめた40日", -19.2, -9.6)]),
    card(f'{icon("Lock", BLUE, 46)}<p style="font-size:30px;font-weight:700;line-height:1.4">過去に合わせすぎない工夫</p>'
         f'<p style="font-size:26px;line-height:1.55">・古い80日で案を選び、新しい40日で確かめる<br>・約20案を比べ、両方の期間で良いものだけ<br>・同じ計算を2回して、一致した結果だけ使う</p>'
         f'<p style="font-size:24px;line-height:1.5;color:{SUB}">デイ守りはリスク0.3%で計測。運用は0.2%なので、40日で約 −6% の見込み</p>',
         bg=PANEL, style="border:none;flex:none;width:440px;gap:18px"),
    gap=28))

# ---------------------------------------------------------------- 07 ミドル → Slack
slack = (f'<div style="width:880px;background:#fff;border:2px solid {LINE};border-radius:24px;padding:30px 34px;gap:16px;box-shadow:0 18px 40px rgba(22,33,58,0.10)">'
         + row(f'<div style="width:64px;height:64px;border-radius:14px;background:{MID};align-items:center;justify-content:center">{icon("Bell", "#fff", 36)}</div>',
               f'<div style="gap:2px"><p style="font-size:26px;font-weight:700">AI Trade Desk <span style="font-size:18px;color:#fff;background:#8A96AD;padding:2px 8px;border-radius:6px">APP</span></p>'
               f'<p style="font-size:20px;color:{SUB}">#ミドル ・ 8:07</p></div>', gap=18, align="center")
         + f'<p style="font-size:30px;line-height:1.5">💡 <b>ミドルの見立て</b> BTC: <b>🟢 買い時の条件あり</b>(自信度 68%)</p>'
           f'<p style="font-size:26px;line-height:1.55;color:#3A4252">現在値 10,300,000円<br>買う目安: 10,560,000円 を上抜けたら<br>損切り -6% ・ 利確 +12%<br>'
           f'理由: 日足が平均線の上に戻り、安値を切り上げた…</p>'
           f'<p style="font-size:22px;color:{SUB}">有効期限 11/19 10:10(自動売買はしていません)</p></div>')
slides["mid"] = page("mid", "ミドル ・ 役割の変更", "売買はやめて、「買い時か」を知らせる係に", row(
    slack,
    f'<div style="flex:1;gap:26px">'
    + card(row(icon("Warning", RED, 40), '<p style="font-size:30px;font-weight:700">なぜやめたか</p>', gap=14, align="center") +
           f'<p style="font-size:28px;line-height:1.5">下落相場では「見送り」が続き、取引が0回。比べることも、育てることもできなかった</p>', top=MID)
    + card(row(icon("CheckCircle", GREEN, 40), '<p style="font-size:30px;font-weight:700">どう使うか</p>', gap=14, align="center") +
           f'<p style="font-size:28px;line-height:1.5">AI の見立て(買い時か・理由・目安の価格)を人が読み、判断の材料にする</p>', top=MID)
    + '</div>', gap=40, align="center"))

# ---------------------------------------------------------------- 08 比べる相手+再スタート
def chip(t, strong=False):
    return (f'<p style="font-size:28px;padding:12px 26px;border-radius:999px;background:{"#FDE7E7" if strong else "#fff"};'
            f'{"font-weight:700;color:" + RED if strong else ""}">{t}</p>')


timeline = (f'<svg width="1600" height="170" viewBox="0 0 1600 170">'
            f'<line x1="40" y1="90" x2="1560" y2="90" stroke="#C9C4B8" stroke-width="6"/>'
            f'<rect x="40" y="70" width="900" height="40" rx="20" fill="#E6E2D8"/>'
            f'<rect x="960" y="70" width="600" height="40" rx="20" fill="{ATTACK}"/>'
            f'<text x="60" y="54" font-size="26" font-weight="700" fill="{SUB}" font-family="Noto Sans JP">v1.0(11/6〜11/17)</text>'
            f'<text x="60" y="150" font-size="24" fill="{SUB}" font-family="Noto Sans JP">記録は「_v1」として別に保存(消さない)</text>'
            f'<circle cx="960" cy="90" r="22" fill="#fff" stroke="{ATTACK}" stroke-width="8"/>'
            f'<text x="990" y="54" font-size="26" font-weight="700" fill="{ATTACK}" font-family="Noto Sans JP">11/17 v1.1 開始</text>'
            f'<text x="990" y="150" font-size="26" font-weight="700" fill="{INK}" font-family="Noto Sans JP">デイの4つの財布を、各100万円から</text></svg>')
slides["compare"] = page("compare", "比べ方を整える", "比べる相手を増やし、100万円から再スタート", card(
    row(f'<p style="font-size:30px;font-weight:700;width:300px">AIなしの比べる相手</p>',
        chip("同じルールだけ(守り)"), chip("同じルールだけ(攻め)"), chip("買って持つだけ"), chip("上げに乗るだけ"),
        chip("下げで売るだけ NEW", True), gap=14, align="center", style="flex-wrap:wrap"),
    bg=PANEL, style="border:none;flex:none") + card(timeline, style="flex:none;align-items:center") +
    row(card(row(icon("Chart", RED, 40), '<p style="flex:1;font-size:28px;line-height:1.5">「下げで売るだけ」は、日足が下向きの間だけ売りで持つ単純なルール。上げの相場の「上げに乗るだけ」と対になる</p>', gap=18, align="center"), style="flex:1"),
        card(row(icon("Database", BLUE, 40), '<p style="flex:1;font-size:28px;line-height:1.5">新しいルールの成績は、始めた日以降の取引だけで測る。過去の期間で良く見せない</p>', gap=18, align="center"), style="flex:1"), gap=28))

# ---------------------------------------------------------------- 09 Webアプリ
slides["web"] = page("web", "Webアプリ", "ログインなしで、デモを誰でも見られるように", row(
    f'<div style="flex:1.6;border-radius:24px;overflow:hidden;border:2px solid {LINE};box-shadow:0 18px 40px rgba(22,33,58,0.12)">'
    + img(sys.argv[2] + "/demo-top.png", "width:100%;display:block") + '</div>',
    f'<div style="flex:1;gap:22px">'
    + card(row(icon("Globe", BLUE, 40), '<p style="font-size:30px;font-weight:700">開くとすぐデモ</p>', gap=14, align="center") +
           '<p style="font-size:26px;line-height:1.5">ログインしていない人には、架空のデータで同じ画面を表示。管理者は右上から本番にログイン</p>')
    + card(row(icon("Lock", BLUE, 40), '<p style="font-size:30px;font-weight:700">本番のデータは出さない</p>', gap=14, align="center") +
           '<p style="font-size:26px;line-height:1.5">デモのデータは、本番と同じ集計のコードで作った架空のもの。費用もかからない</p>')
    + card(row(icon("Chart", BLUE, 40), '<p style="font-size:30px;font-weight:700">v1.1 の表示</p>', gap=14, align="center") +
           '<p style="font-size:26px;line-height:1.5">版の表示、変更のお知らせ、「下げで売るだけ」の線を追加</p>')
    + '</div>', gap=36, align="center"))

# ---------------------------------------------------------------- 10 これから
def goal(ic, title, body, color):
    return card(f'{icon(ic, color, 52)}<p style="font-size:34px;font-weight:700">{title}</p><p style="font-size:28px;line-height:1.5;color:{SUB}">{body}</p>', top=color, style="gap:18px")


slides["next"] = page("next", "これから測ること", "AIは「同じルールだけ」に勝てるか", row(
    goal("Clock", "8週間・100回", "決めておいた基準で測る。結果を見てから基準を変えない", BLUE),
    goal("Users", "AIの見送りの価値", "指標の前や急落の最中に「入らない」判断が、損失を減らせるか", ATTACK),
    goal("Shield", "下落の大きさ", "デイ守りは小さく、デイ攻めは停止ラインの内側で", GUARD),
    gap=28) + row(
    f'<div style="flex:1;background:{NAVY};border-radius:24px;padding:30px 40px;flex-direction:row;align-items:center;gap:24px">'
    f'{icon("Lightbulb", "#F2B27A", 48)}<p style="font-size:32px;color:#F6F4EE;line-height:1.5">負けたことも記録に残し、<b style="color:#F2B27A">調べて・直して・測り直す</b>。この繰り返しを仕組みにしている</p></div>'))

order = ["cover", "oneline", "v10", "why", "attack", "guard", "backtest", "mid", "compare", "web", "next"]
for sid in order:
    (OUT / f"{sid}.html").write_text(slides[sid], encoding="utf-8")
(OUT / "order.txt").write_text("\n".join(order), encoding="utf-8")
print("ok", len(order))
