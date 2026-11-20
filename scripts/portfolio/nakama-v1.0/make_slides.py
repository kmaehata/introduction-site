# NAKAMA v1.0 の資料(アーキテクチャ・処理の流れ)のスライド HTML を作る。
# 使い方: python make_slides.py <出力フォルダ> <スクリーンショットのあるフォルダ>
# 見た目は AIトレードデスクの資料に合わせる。図はすべて HTML と SVG で描く。
import base64
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
SHOTS = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

NAVY, INK, SUB, BG, CARD, LINE = "#16213A", "#1B2440", "#5B6478", "#F4F2EE", "#FDFCF8", "#E2DED3"
ACCENT, BLUE, RED, GREEN, GRAY = "#C8641E", "#2A78D6", "#D2433B", "#1E8E5A", "#8A93A6"
REN, MIRU, GEM = "#6B4FBB", "#D9578F", "#2A78D6"
REN_S, MIRU_S, GEM_S, PANEL, WARM, GREEN_S, RED_S = "#E9E4F7", "#FBE3EE", "#E1ECFA", "#E9EEF6", "#FBE6D5", "#DCF1E6", "#FBE2E0"
HEAD = "font-family:'Zen Maru Gothic','Noto Sans JP',sans-serif;font-weight:700"
BODY = "font-family:'Noto Sans JP',sans-serif"


def page(sid, eyebrow, title, inner, bg=BG, gap=40):
    return (f'<section id="{sid}" style="background:{bg};color:{INK};{BODY};padding:96px 120px 72px;'
            f'display:flex;flex-direction:column;gap:{gap}px">'
            f'<div style="gap:12px"><p style="font-size:26px;font-weight:700;color:{ACCENT}">{eyebrow}</p>'
            f'<h2 style="{HEAD};font-size:60px;color:{INK}">{title}</h2></div>{inner}</section>')


def row(*children, gap=28, align="stretch", style=""):
    return f'<div style="display:flex;flex-direction:row;gap:{gap}px;align-items:{align};{style}">{"".join(children)}</div>'


def col(*children, gap=16, style=""):
    return f'<div style="gap:{gap}px;{style}">{"".join(children)}</div>'


def card(inner, top=None, bg=CARD, style=""):
    border = f"border-top:12px solid {top};" if top else ""
    return (f'<div style="flex:1;background:{bg};border:2px solid {LINE};{border}border-radius:26px;padding:28px 32px;'
            f'gap:14px;{style}">{inner}</div>')


def pill(text, fg, bg, size=24):
    return f'<p style="font-size:{size}px;font-weight:700;color:{fg};background:{bg};padding:5px 20px;border-radius:999px;white-space:nowrap">{text}</p>'


def icon(name, color, size=40):
    return f'<x-icon name="{name}" style="width:{size}px;height:{size}px;color:{color}"></x-icon>'


def badge(name, color, soft, size=72):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{soft};align-items:center;'
            f'justify-content:center;flex:none">{icon(name, color, int(size * 0.52))}</div>')


def h3(text, size=40, color=INK):
    return f'<h3 style="{HEAD};font-size:{size}px;color:{color}">{text}</h3>'


def p(text, size=28, color=INK, weight=400, style=""):
    return f'<p style="font-size:{size}px;color:{color};font-weight:{weight};{style}">{text}</p>'


def tile(title, sub, bg="#24314F", fg="#F6F4EE", subc="#AEB8CC", ic=None, icc="#F2B27A"):
    head = row(icon(ic, icc, 32), f'<p style="font-size:28px;font-weight:700;color:{fg}">{title}</p>', gap=10, align="center") if ic \
        else f'<p style="font-size:28px;font-weight:700;color:{fg}">{title}</p>'
    return (f'<div style="flex:1;background:{bg};border-radius:18px;padding:16px 20px;gap:4px">{head}'
            f'<p style="font-size:22px;color:{subc};line-height:1.35">{sub}</p></div>')


def arrow(label="", length=110, color=GRAY, both=False, vertical=False):
    """ラベル付きの矢印。both=True で両向き。"""
    if vertical:
        svg = (f'<svg width="28" height="{length}" viewBox="0 0 28 {length}">'
               f'<line x1="14" y1="{6 if both else 0}" x2="14" y2="{length - 10}" stroke="{color}" stroke-width="4"/>'
               f'<polygon points="4,{length - 14} 24,{length - 14} 14,{length}" fill="{color}"/>'
               + (f'<polygon points="4,14 24,14 14,0" fill="{color}"/>' if both else "") + '</svg>')
        return row(svg, f'<p style="font-size:22px;color:{SUB};line-height:1.3">{label}</p>', gap=10, align="center")
    svg = (f'<svg width="{length}" height="28" viewBox="0 0 {length} 28">'
           f'<line x1="{12 if both else 0}" y1="14" x2="{length - 12}" y2="14" stroke="{color}" stroke-width="4"/>'
           f'<polygon points="{length - 16},4 {length - 16},24 {length},14" fill="{color}"/>'
           + (f'<polygon points="16,4 16,24 0,14" fill="{color}"/>' if both else "") + '</svg>')
    return (f'<div style="align-items:center;justify-content:center;gap:8px;flex:none">'
            f'<p style="font-size:22px;color:{SUB};text-align:center;line-height:1.3">{label}</p>{svg}</div>')


def img(path, style):
    data = base64.b64encode(Path(path).read_bytes()).decode()
    return f'<img src="data:image/png;base64,{data}" style="{style}">'


def cover(sid, no, title, catch, audience, toc, right_extra=""):
    items = "".join(
        f'<div style="display:flex;flex-direction:row;align-items:center;gap:20px;border-bottom:1px solid #2E3D63;padding:10px 0px">'
        f'<p style="width:52px;font-size:24px;font-weight:700;color:#8FB4FF">{i + 1:02d}</p>'
        f'<p style="font-size:28px;color:#E6EBF5">{t}</p></div>' for i, t in enumerate(toc))
    return (
        f'<section id="{sid}" style="background:{NAVY};color:#F6F4EE;{BODY};padding:100px 120px;display:flex;flex-direction:row;align-items:center;gap:90px">'
        f'<div style="width:760px;gap:26px"><p style="font-size:28px;font-weight:700;letter-spacing:2px;color:#8FB4FF">NAKAMA ・ Version 1.0</p>'
        f'<p style="{HEAD};font-size:120px;line-height:1;color:#3A4A6B">{no}</p>'
        f'<h1 style="{HEAD};font-size:88px;line-height:1.2">{title}</h1>'
        f'<p style="font-size:36px;line-height:1.5;color:#C9D3E6">{catch}</p>'
        f'{row(*[pill(a, NAVY, "#8FB4FF") for a in audience], gap=12)}</div>'
        f'<div style="flex:1;gap:22px">{right_extra}'
        f'<p style="font-size:24px;font-weight:700;letter-spacing:4px;color:#8A96AD">CONTENTS</p><div style="gap:2px">{items}</div></div></section>')


slides = {}

# ================================================================ 01 アーキテクチャ
arch_toc = ["全体のしくみ", "なぜ GCP と Gemini Live なのか", "実際の構成(GCP)", "画面の中のしくみ", "お金の守り方"]
slides["cover-arch"] = cover(
    "cover-arch", "01", "アーキテクチャ", "声で話すAIを、使わない日は0円で動かす", ["エンジニア向け"], arch_toc,
    right_extra=img(SHOTS / "ren-talking.png", "width:100%;border-radius:20px;border:2px solid #2E3D63"))

# ---------------------------------------------------------------- 全体のしくみ
you = card(
    row(badge("Users", ACCENT, WARM, 64), h3("あなた", 40), gap=16, align="center") +
    p("スマホ・PC のブラウザ", 24, SUB) +
    col(row(icon("Chat", ACCENT, 30), p("マイクで話す", 26), gap=10, align="center"),
        row(icon("Play", ACCENT, 30), p("声と字幕で聞く", 26), gap=10, align="center"),
        row(icon("Star", ACCENT, 30), p("3Dのキャラが反応", 26), gap=10, align="center"), gap=10),
    bg="#FFF6EE", style="flex:none;width:330px")
relay = (
    f'<div style="flex:none;width:620px;background:{NAVY};border-radius:26px;padding:28px 30px;gap:16px">'
    + row(p("中継係", 34, "#F6F4EE", 700), pill("Cloud Run", NAVY, "#8FB4FF", 22), gap=14, align="center", style="justify-content:space-between")
    + row(tile("本人確認", "知らないサイトや<br>ボットを入れない", ic="Lock"), tile("中継", "声をそのまま<br>受け渡す", ic="Link"), gap=14)
    + row(tile("性格を渡す", "性格と記憶を<br>最初に渡す", ic="Book"), tile("料金メーター", "使った量を<br>すぐ金額にする", ic="Chart"), gap=14)
    + '</div>')
gem = card(
    row(badge("Lightbulb", GEM, "#FFFFFF", 60), h3("Gemini 3.8 Live", 31), gap=12, align="center") +
    p("Google の音声AI", 24, SUB) +
    f'<div style="background:#FFFFFF;border-radius:18px;padding:16px 20px;gap:6px">'
    f'{p("聞く・考える・話す", 30, GEM, 700)}{p("を1つのAIで行う", 26)}</div>' +
    row(icon("Search", GEM, 28), p("時事ネタは Google 検索", 24), gap=10, align="center"),
    bg=GEM_S, style="flex:none;width:400px")
top = row(you, arrow("声・文字<br>WebSocket", 120, both=True), relay, arrow("声のまま", 120, both=True), gem, gap=14, align="center")
store = card(
    row(icon("Database", GREEN, 40), h3("Firestore", 34), pill("無料枠", GREEN, GREEN_S, 20), gap=14, align="center") +
    p("覚えたこと・親密度 / 今日と今月の利用額 / 非常停止のスイッチ", 24, SUB),
    style="flex:none;width:780px;margin-left:370px")
guard = card(
    row(icon("Trust", RED, 40), h3("お金の見張り", 34), gap=14, align="center") +
    p("GCP の請求が月750円を超えたら<br>自動で公開を止める", 24, SUB),
    bg="#FFF7F5", style="flex:1")
bottom = row(store, guard, gap=28)
slides["arch-overview"] = page("arch-overview", "アーキテクチャの概要", "全体のしくみ",
                               top + f'<div style="margin-left:900px;margin-top:-24px">{arrow("記憶・利用額を読み書き", 70, vertical=True, both=True)}</div>' + bottom,
                               gap=30)


# ---------------------------------------------------------------- なぜ GCP と Gemini Live なのか
def step(label, sub, color, soft):
    return (f'<div style="flex:1;background:{soft};border-radius:18px;padding:16px 18px;gap:4px;align-items:center">'
            f'<p style="font-size:28px;font-weight:700;color:{color}">{label}</p><p style="font-size:22px;color:{SUB}">{sub}</p></div>')


def mini_arrow():
    return f'<div style="justify-content:center">{arrow("", 56)}</div>'


aws_pipe = row(step("文字にする", "Transcribe", GRAY, "#ECEAE4"), mini_arrow(), step("考える", "Claude", GRAY, "#ECEAE4"),
               mini_arrow(), step("声にする", "ElevenLabs", GRAY, "#ECEAE4"), gap=8)
gcp_pipe = row(step("聞く・考える・話す", "Gemini 3.8 Live(1つのAI)", GEM, GEM_S), gap=8)


def judge(rows_):
    out = ""
    for k, v, good in rows_:
        mark = icon("CheckCircle", GREEN, 30) if good else icon("Warning", ACCENT, 30)
        out += row(mark, p(k, 24, SUB, style="width:150px"), p(v, 26, INK, 500), gap=12, align="center")
    return col(out, gap=12)


aws_card = card(
    row(h3("AWS で作る場合", 36, SUB), pill("比べた案", SUB, "#ECEAE4", 20), gap=14, align="center") + aws_pipe +
    judge([("返事の速さ", "約1.2〜1.8秒(3回の受け渡し)", False),
           ("声の調子", "一度文字にするので、感情が落ちやすい", False),
           ("割り込み", "自分で作り込みが必要", False),
           ("待機の費用", "常に動くサーバーで月25ドル前後〜", False)]))
gcp_card = card(
    row(h3("今回の作り(GCP)", 36, GEM), pill("採用", "#FFFFFF", GEM, 20), gap=14, align="center") + gcp_pipe +
    judge([("返事の速さ", "実測 約0.7〜1.2秒", True),
           ("声の調子", "声のまま理解し、声で返す", True),
           ("割り込み", "標準で対応", True),
           ("待機の費用", "呼ばれた時だけ動く。ほぼ0円", True)]),
    top=GEM)
slides["arch-why"] = page("arch-why", "技術の選び方", "掛け合いはテンポが命。だから声のまま返すAIにした",
                          row(aws_card, gcp_card, gap=32) +
                          row(*[f'<div style="flex:1;background:{NAVY};border-radius:22px;padding:22px 28px;gap:6px">'
                                f'<p style="font-size:22px;font-weight:700;color:#8FB4FF">決め手 {n}</p>'
                                f'<p style="{HEAD};font-size:36px;color:#F6F4EE">{t}</p><p style="font-size:22px;color:#AEB8CC">{d}</p></div>'
                                for n, t, d in [("1", "テンポ", "悪口の言い合いは、返事の速さと間で面白さが決まる"),
                                                ("2", "使わない日は0円", "ポートフォリオなので、見られない日の費用をなくしたい"),
                                                ("3", "1社で完結", "音声AI・サーバー・保存先・お金の見張りが GCP だけで揃う")]], gap=24) +
                          p("日本語で「声のまま会話できるAI」は、検討した時点で AWS には無かった(Nova Sonic は日本語に未対応)。", 22, SUB),
                          gap=34)


# ---------------------------------------------------------------- 実際の構成(GCP)
def res(ic, color, name, svc, lines, soft=CARD, style=""):
    body = "".join(p(f"・{l}", 22, SUB) for l in lines)
    return (f'<div style="flex:1;background:{soft};border:2px solid {LINE};border-radius:22px;padding:20px 24px;gap:8px;{style}">'
            + row(icon(ic, color, 34), f'<p style="font-size:28px;font-weight:700">{name}</p>', gap=12, align="center")
            + f'<p style="font-size:22px;font-weight:700;color:{color}">{svc}</p>{body}</div>')


def group(title, color, *children, style=""):
    return (f'<div style="flex:1;border:3px dashed {color};border-radius:28px;padding:18px 20px 20px;gap:14px;{style}">'
            f'<p style="font-size:24px;font-weight:700;color:{color}">{title}</p>{"".join(children)}</div>')


run = res("Cloud", BLUE, "公開する", "Cloud Run ・ nakama-ag",
          ["us-central1(AIと同じ場所)", "最小0台・最大1台", "画面とAPIを1つの箱で配信", "会話は WebSocket で最大60分"], soft="#F3F7FD")
ai = res("Lightbulb", GEM, "話すAI", "Vertex AI ・ gemini-3.8-live",
         ["声: レン=Orus / ミル=Leda", "表情・記憶などの道具4つ", "Google 検索"], soft=GEM_S)
fs = res("Database", GREEN, "覚える", "Firestore(無料枠)",
         ["users … 親密度・呼び名・記憶", "usage … 日・月の利用額", "config … 停止スイッチ・流行語"])
build = res("Wrench", SUB, "作って置く", "Cloud Build → Artifact Registry",
            ["Dockerfile で画面とサーバーを1つに", "古いイメージは自動で消す(最新2つ)"])
budget = res("Warning", RED, "見張る", "Cloud Billing の予算 → Pub/Sub",
             ["月750円(約5ドル)", "50% / 90% / 100% で通知"], soft="#FFF7F5")
kill = res("Lock", RED, "止める", "Cloud Functions ・ nakama-killswitch",
           ["100% で停止スイッチを入れる", "公開設定(allUsers)を外す"], soft="#FFF7F5")
iam = res("Key", ACCENT, "権限は最小", "専用のサービスアカウント",
          ["実行用: AIの利用と Firestore だけ", "停止用: 停止に必要な権限だけ"])
slides["arch-gcp"] = page("arch-gcp", "実際の構成", "GCP の上で、こう組んでいる", row(
    group("会話を動かす", BLUE, row(run, ai, gap=16), row(fs, build, gap=16),
          row(p("通り道", 22, BLUE, 700, "width:90px"),
              *[x for pair in zip([pill(t, INK, "#FFFFFF", 22) for t in ["ブラウザ", "Cloud Run", "Vertex AI"]],
                                  [arrow("", 40), arrow("", 40), ""]) for x in pair if x],
              p("記憶と利用額は Firestore へ", 22, SUB, style="margin-left:18px"), gap=10, align="center",
              style="background:#EEF3FB;border-radius:16px;padding:14px 18px;margin-top:auto"),
          style="flex:2"),
    group("お金と安全を守る", RED, budget, kill, iam),
    gap=24, style="flex:1"), gap=30)


# ---------------------------------------------------------------- 画面の中のしくみ
def chip(n, title, sub, color, soft):
    return (f'<div style="flex:1;background:{soft};border-radius:20px;padding:22px 22px;gap:6px">'
            f'<p style="font-size:22px;font-weight:700;color:{color}">{n}</p>'
            f'<p style="font-size:28px;font-weight:700">{title}</p><p style="font-size:22px;color:{SUB};line-height:1.4">{sub}</p></div>')


def lane(label, color, *chips_):
    items = []
    for i, c in enumerate(chips_):
        items.append(c)
        if i < len(chips_) - 1:
            items.append(f'<div style="justify-content:center">{arrow("", 44)}</div>')
    return row(f'<div style="width:190px;justify-content:center"><p style="{HEAD};font-size:34px;color:{color}">{label}</p></div>',
               *items, gap=10)


slides["arch-browser"] = page("arch-browser", "ブラウザの中", "画面の中では、3つのことを同時にしている", col(
    lane("聞く", ACCENT,
         chip("① マイク", "音を拾う", "雑音とエコーを<br>ブラウザが消す", ACCENT, WARM),
         chip("② 整える", "16kHz の音に", "AudioWorklet で<br>20ミリ秒ごとに切る", ACCENT, WARM),
         chip("③ 区切る", "話す間だけ送る", "0.65秒静かなら<br>話し終わり", ACCENT, WARM),
         chip("④ 送る", "サーバーへ", "無音は送らない<br>= 無音は課金されない", ACCENT, WARM)),
    lane("話す", GEM,
         chip("① 受け取る", "24kHz の声", "届いた順に<br>すき間なく並べる", GEM, GEM_S),
         chip("② 鳴らす", "スピーカーへ", "割り込まれたら<br>すぐ捨てる", GEM, GEM_S),
         chip("③ 測る", "声の大きさ", "毎フレーム<br>音量を読む", GEM, GEM_S),
         chip("④ 動かす", "口パク", "大きい声ほど<br>口を開ける", GEM, GEM_S)),
    lane("見せる", REN,
         chip("3Dのキャラ", "VRM モデル", "表情・瞬き・呼吸・<br>カメラ目線", REN, REN_S),
         chip("背景", "キャラごとに", "レン: 雨の夜の屋上<br>ミル: 日差しの部屋", REN, REN_S),
         chip("演出", "ボケと光", "背景をぼかして<br>キャラを引き立てる", REN, REN_S),
         chip("技術", "React Three Fiber", "three.js と<br>three-vrm で描く", REN, REN_S)),
    f'<div style="background:{NAVY};border-radius:20px;padding:18px 28px;display:flex;flex-direction:row;align-items:center;gap:18px">'
    f'{icon("Star", "#F2B27A", 36)}<p style="font-size:24px;color:#E6EBF5">3Dのキャラは VRoid Studio で作る VRM を読み込む。モデルが無いときは、声に合わせて光る球で代わりに表示する。</p></div>',
    gap=22), gap=34)


# ---------------------------------------------------------------- お金の守り方
def shield(n, title, value, note, color, soft, width):
    return (f'<div style="width:{width}px;background:{soft};border-left:12px solid {color};border-radius:18px;padding:28px 28px;'
            f'display:flex;flex-direction:row;align-items:center;gap:22px">'
            f'<p style="{HEAD};font-size:48px;color:{color};width:46px">{n}</p>'
            f'<div style="flex:1;gap:6px"><p style="font-size:34px;font-weight:700">{title}</p><p style="font-size:23px;color:{SUB};line-height:1.45">{note}</p></div>'
            f'<p style="font-size:30px;font-weight:700;color:{color};white-space:nowrap">{value}</p></div>')


stack = col(
    shield("1", "入口", "ボット対策", "Firebase の匿名ログインと App Check(必要になったら有効化)", GRAY, "#ECEAE4", 1060),
    shield("2", "1人あたり", "1回3分・1日5分", "1人で上限を使い切らせない", BLUE, "#E1ECFA", 1000),
    shield("3", "アプリのメーター", "1日1ドル・月4.5ドル", "AIが返す利用量をすぐ金額にして足す。超えそうならキャラが別れを告げて終了", GREEN, GREEN_S, 940),
    shield("4", "最後の保険", "月750円", "GCP の請求額で判定。通知は数時間遅れるので、メーターが壊れた時の保険", RED, RED_S, 880),
    gap=20)
fact = card(
    h3("実測", 36) +
    col(row(p("1往復", 26, SUB, style="width:170px"), p("約0.004ドル(約0.6円)", 30, INK, 700), align="center"),
        row(p("1日1ドルで", 26, SUB, style="width:170px"), p("約40分話せる", 30, INK, 700), align="center"),
        row(p("使わない日", 26, SUB, style="width:170px"), p("ほぼ0円", 30, GREEN, 700), align="center"), gap=14) +
    f'<div style="background:{PANEL};border-radius:16px;padding:16px 20px;gap:6px">'
    f'{p("Cloud Run は呼ばれた時だけ動く", 24, INK, 700)}{p("EC2 のように動き続けないので、待機中の費用がかからない", 22, SUB)}</div>' +
    f'<div style="background:{RED_S};border-radius:16px;padding:16px 20px;gap:6px">'
    f'{p("止まることも確かめた", 24, RED, 700)}{p("予算超過の通知を送り、公開URLが閉じる→元に戻す、まで試した", 22, SUB)}</div>',
    style="flex:none;width:600px;align-self:stretch;justify-content:space-between")
slides["arch-cost"] = page("arch-cost", "お金の守り方", "4段の守りで、月5ドルを超えないようにする",
                           row(stack, fact, gap=36, align="flex-start"), gap=36)

# ================================================================ 02 処理の流れ
flow_toc = ["1回の会話の流れ", "話の途中で割り込める", "会話を止めずに、裏で道具を使う", "キャラの性格の組み立て方",
            "上限に近づいたとき", "長く話しても途切れない工夫"]
slides["cover-flow"] = cover("cover-flow", "02", "処理の流れ", "話しかけてから、返事が聞こえるまで",
                             ["エンジニア向け", "ビジネス向け"], flow_toc)


# ---------------------------------------------------------------- 1回の会話の流れ
def big_step(n, who, color, soft, ic, title, sub):
    return (f'<div style="flex:1;background:{CARD};border:2px solid {LINE};border-top:12px solid {color};border-radius:24px;padding:22px 22px;gap:10px">'
            + row(f'<p style="{HEAD};font-size:40px;color:{color}">{n}</p>', pill(who, color, soft, 20), gap=10, align="center", style="justify-content:space-between")
            + f'<div style="align-items:flex-start">{badge(ic, color, soft, 64)}</div>'
            + f'<p style="font-size:30px;font-weight:700">{title}</p><p style="font-size:22px;color:{SUB};line-height:1.45">{sub}</p></div>')


steps = row(
    big_step("1", "あなた", ACCENT, WARM, "Chat", "話す", "マイクの音を、<br>話している間だけ送る"),
    big_step("2", "ブラウザ", ACCENT, WARM, "Clock", "区切る", "0.65秒静かなら<br>「話し終わり」と合図"),
    big_step("3", "Cloud Run", BLUE, "#E1ECFA", "Link", "中継する", "性格・記憶を最初に渡し、<br>あとは声を受け渡すだけ"),
    big_step("4", "Gemini", GEM, GEM_S, "Lightbulb", "考えて話す", "声のまま理解し、<br>声で返事を作る"),
    big_step("5", "ブラウザ", REN, REN_S, "Play", "届く", "声・字幕・表情。<br>声の大きさで口が動く"),
    gap=16)
bar = (f'<div style="background:{NAVY};border-radius:24px;padding:24px 36px;display:flex;flex-direction:row;align-items:center;gap:40px">'
       f'<div style="gap:4px"><p style="font-size:24px;color:#AEB8CC">話し終わってから、返事が聞こえ始めるまで(実測)</p>'
       f'<p style="{HEAD};font-size:64px;color:#F6F4EE">約 0.7〜1.2 秒</p></div>'
       f'<div style="flex:1;gap:10px">'
       f'<div style="background:#24314F;border-radius:14px;padding:12px 18px"><p style="font-size:24px;color:#E6EBF5">あなた「ゲームでボロ負けした」</p></div>'
       f'<div style="background:{REN};border-radius:14px;padding:12px 18px"><p style="font-size:24px;color:#FFFFFF">レン「は？ボロ負けって、どんだけ下手なんだよ。ドンマイ。」</p></div></div></div>')
fast = row(*[card(row(icon(ic, c, 34), h3(t, 30), gap=12, align="center") + p(d, 23, SUB), style="padding:22px 26px")
             for ic, c, t, d in [("Clock", ACCENT, "待ちすぎない", "0.65秒の静けさで話し終わりと判断。長く待つと、返事が遅く感じる"),
                                 ("Lightning", GEM, "文字を経由しない", "声を文字にして、また声にする手間がない分だけ速い"),
                                 ("Play", REN, "届いたらすぐ鳴らす", "返事を最後まで待たず、最初の声が届いた瞬間に再生する")]], gap=20)
slides["flow-turn"] = page("flow-turn", "1回の会話の流れ", "話しかけてから、返事が聞こえるまで", steps + bar + fast, gap=28)


# ---------------------------------------------------------------- 割り込み
def tl_row(label, color, bars):
    inner = "".join(
        f'<div style="position:absolute;left:{l}px;width:{w}px;top:12px;height:60px;border-radius:14px;background:{c};'
        f'{"opacity:.35;" if faded else ""}align-items:flex-start;justify-content:center;padding:0 16px">'
        f'<p style="font-size:24px;color:#FFFFFF;font-weight:700;white-space:nowrap">{t}</p></div>'
        for l, w, c, t, faded in bars)
    return row(f'<div style="width:200px;justify-content:center"><p style="font-size:28px;font-weight:700;color:{color}">{label}</p></div>',
               f'<div style="position:relative;flex:1;height:84px;background:#ECEAE4;border-radius:16px">{inner}</div>', gap=16)


def marker(x, n, text, color):
    return (f'<div style="position:absolute;left:{x}px;top:0px;bottom:0px;width:3px;background:{color}"></div>'
            f'<div style="position:absolute;left:{x - 22}px;top:-10px;width:46px;height:46px;border-radius:50%;background:{color};align-items:center;justify-content:center">'
            f'<p style="font-size:24px;font-weight:700;color:#FFFFFF">{n}</p></div>')


timeline = (
    f'<div style="position:relative;padding:44px 0px 10px;gap:22px">'
    + tl_row("キャラの声", REN, [(20, 640, REN, "いや、それはお前の練習不足だろ。だいたい", False), (660, 520, REN, "(言うはずだった続き)", True),
                                (1060, 400, REN, "は？言い訳か？", False)])
    + tl_row("あなた", ACCENT, [(560, 380, ACCENT, "待って、相手がチートだった", False)])
    + f'<div style="position:absolute;left:216px;top:0px;right:0px;bottom:0px">{marker(560, "1", "", ACCENT)}{marker(600, "2", "", RED)}{marker(980, "3", "", GEM)}</div>'
    + '</div>')
expl = row(
    card(row(f'<p style="{HEAD};font-size:40px;color:{ACCENT}">1</p>', h3("話し始める", 32), gap=12, align="center") +
         p("声が一定の大きさを超えたら「話し始めた」と判定。キャラが話している間は、自分の声を拾わないよう基準を上げる。", 24, SUB)),
    card(row(f'<p style="{HEAD};font-size:40px;color:{RED}">2</p>', h3("手元ですぐ止める", 32), gap=12, align="center") +
         p("サーバーの返事を待たず、ブラウザが再生中の声をその場で捨てる。だから人と話すときのように、すぐ黙る。", 24, SUB)),
    card(row(f'<p style="{HEAD};font-size:40px;color:{GEM}">3</p>', h3("新しい話に返す", 32), gap=12, align="center") +
         p("Gemini も話すのをやめて、割り込んだ内容を聞いてから返事を作り直す。", 24, SUB)),
    gap=24)
note = (f'<div style="background:{NAVY};border-radius:20px;padding:20px 30px;display:flex;flex-direction:row;align-items:center;gap:18px">'
        f'{icon("Lightning", "#F2B27A", 36)}<p style="font-size:24px;color:#E6EBF5">話し始めは 60ミリ秒(20ミリ秒 × 3回)続いたら判定。声が出た瞬間に、キャラの声が止まる。</p></div>')
slides["flow-interrupt"] = page("flow-interrupt", "割り込み", "話の途中で割り込んでも、すぐ黙って聞き直す", timeline + expl + note, gap=40)


# ---------------------------------------------------------------- 道具
def tool(ic, color, soft, name, what, shows):
    return row(badge(ic, color, soft, 64),
               f'<div style="flex:1;gap:2px"><p style="font-size:28px;font-weight:700">{what}</p>'
               f'<p style="font-size:20px;color:{SUB};font-family:monospace">{name}</p></div>',
               pill(shows, color, soft, 20), gap=18, align="center",
               style=f"background:{CARD};border:2px solid {LINE};border-radius:20px;padding:20px 24px")


tools = col(
    tool("Star", REN, REN_S, "set_mood", "表情を変える", "顔が変わる"),
    tool("Book", GREEN, GREEN_S, "remember_fact", "相手のことを覚える", "「覚えた」と表示"),
    tool("Users", ACCENT, WARM, "set_nickname", "呼び名を覚える", "次から名前で呼ぶ"),
    tool("Activity", MIRU, MIRU_S, "adjust_affinity", "親密度を上げる", "いじりが強くなる"),
    tool("Search", GEM, GEM_S, "google_search", "ニュースや天気を調べる", "時事ネタで話す"),
    gap=18, style="flex:1")


def ba(label, color, soft, text):
    return (f'<div style="background:{soft};border-radius:16px;padding:14px 18px;gap:4px">'
            f'<p style="font-size:22px;font-weight:700;color:{color}">{label}</p><p style="font-size:24px;line-height:1.45">{text}</p></div>')


trouble = card(
    row(icon("Wrench", ACCENT, 36), h3("作っていてつまずいた点", 32), gap=12, align="center") +
    p("道具は「会話を止めない呼び方」(非同期)にしている。結果を返すとき「黙って受け取って」と伝えるのが基本。", 24, SUB) +
    ba("起きたこと", RED, RED_S, "キャラが<b>話し始める前に</b>表情を変えると、<br>そのまま黙ってターンが終わった") +
    f'<div style="align-items:center">{icon("ArrowDown", ACCENT, 40)}</div>' +
    ba("直し方", GREEN, GREEN_S, "まだ声が出ていなければ、<br>「受け取ったら話して」と返すように変えた") +
    p("話している途中なら黙って受け取り、話す前なら受け取ったあとに話す。", 22, SUB),
    style="flex:none;width:720px")
slides["flow-tools"] = page("flow-tools", "道具の使い方", "会話を止めずに、裏で道具を使う", row(tools, trouble, gap=32, align="flex-start"), gap=34)


# ---------------------------------------------------------------- 性格の組み立て
def layer(title, sub, color, soft, w):
    return (f'<div style="width:{w}px;align-self:center;background:{soft};border-left:10px solid {color};border-radius:14px;padding:16px 22px;'
            f'display:flex;flex-direction:row;align-items:center;gap:18px">'
            f'<p style="font-size:26px;font-weight:700;width:230px">{title}</p><p style="font-size:22px;color:{SUB}">{sub}</p></div>')


layers = col(
    layer("人格", "レン: 口が悪い超辛口 / ミル: ゆるふわ", REN, REN_S, 900),
    layer("今の状況", "日付と時刻・今日で何回目の会話か", BLUE, "#E1ECFA", 900),
    layer("距離感", "親密度(0〜100)で呼び方といじりの強さが変わる", MIRU, MIRU_S, 900),
    layer("辛口レベル", "画面のスライダー(0〜100)。会話中も変えられる", ACCENT, WARM, 900),
    layer("覚えていること", "名前・好きなもの・最近の出来事(最新12件)", GREEN, GREEN_S, 900),
    layer("流行語", "ドンマイ・それってあなたの感想ですよね・冗談だよ など", GEM, GEM_S, 900),
    layer("話し方", "1回1〜3文。記号や絵文字は使わない(読み上げるため)", GRAY, "#ECEAE4", 900),
    f'<div style="width:900px;align-self:center;background:{RED};border-radius:14px;padding:12px 22px;display:flex;flex-direction:row;align-items:center;gap:18px">'
    f'{icon("Trust", "#FFFFFF", 34)}<p style="font-size:26px;font-weight:700;color:#FFFFFF;width:196px">越えない線</p>'
    f'<p style="font-size:22px;color:#FFE9E7">容姿や属性はいじらない・落ち込んだら寄り添う</p></div>',
    gap=10, style="flex:none")
chars = col(
    card(row(f'<div style="width:64px;height:64px;border-radius:50%;background:{REN}"></div>', h3("レン", 40), pill("ドS", REN, REN_S, 20), gap=14, align="center") +
         p("声: Orus。短く言い切る。<br>褒められると「うるせ」", 24, SUB), top=REN),
    card(row(f'<div style="width:64px;height:64px;border-radius:50%;background:{MIRU}"></div>', h3("ミル", 40), pill("ゆるふわ", MIRU, MIRU_S, 20), gap=14, align="center") +
         p("声: Leda。全部肯定してから、<br>ふわっと刺す", 24, SUB), top=MIRU),
    card(p("実際の会話(辛口50)", 22, SUB, 700) +
         f'<div style="background:#ECEAE4;border-radius:14px;padding:10px 16px"><p style="font-size:22px">あなた「お前だって弱いだろ」</p></div>'
         f'<div style="background:{REN};border-radius:14px;padding:10px 16px"><p style="font-size:22px;color:#FFFFFF">レン「は？俺が弱い？ それってあなたの感想ですよね。」</p></div>'
         f'<div style="background:#ECEAE4;border-radius:14px;padding:10px 16px"><p style="font-size:22px">あなた「俺の名前はこうせい。覚えといて」</p></div>'
         f'<div style="background:{REN};border-radius:14px;padding:10px 16px"><p style="font-size:22px;color:#FFFFFF">レン「わかったよ、こうせい。次からはそう呼んでやる。」</p></div>',
         style="gap:10px"),
    gap=16, style="flex:1")
slides["flow-persona"] = page("flow-persona", "キャラの作り方", "性格は、8つの層を重ねて毎回組み立てる", row(layers, chars, gap=36, align="flex-start"), gap=32)


# ---------------------------------------------------------------- 上限
def node(text, sub, color, soft, w=270):
    return (f'<div style="flex:1;background:{soft};border-radius:20px;padding:24px 24px;gap:8px">'
            f'<p style="font-size:28px;font-weight:700;color:{color}">{text}</p><p style="font-size:23px;color:{SUB};line-height:1.45">{sub}</p></div>')


meter = row(
    node("① 利用量が届く", "Gemini が1往復ごとに<br>使ったトークン数を返す", GEM, GEM_S),
    arrow("", 50),
    node("② 金額にする", "声と文字で単価を分けて<br>ドルに換算", BLUE, "#E1ECFA"),
    arrow("", 50),
    node("③ 合計に足す", "今日と今月の合計を<br>Firestore に足す", GREEN, GREEN_S),
    arrow("", 50),
    node("④ 上限の手前なら", "キャラが一言で別れを告げ、<br>8秒以内に切断", REN, REN_S, 320),
    gap=10, align="center")
say = row(
    f'<div style="flex:1;background:{REN};border-radius:16px;padding:14px 20px"><p style="font-size:24px;color:#FFFFFF">レン「今日はもう店じまい。また明日な」</p></div>',
    f'<div style="flex:1;background:{MIRU};border-radius:16px;padding:14px 20px"><p style="font-size:24px;color:#FFFFFF">ミル「今日はいっぱい話したね〜、また明日〜」</p></div>',
    gap=18)
kill_flow = row(
    node("予算超過の通知", "GCP の予算 → Pub/Sub", RED, RED_S, 280), arrow("", 46),
    node("非常停止の関数", "停止スイッチを入れ、<br>公開設定を外す", RED, RED_S, 280), arrow("", 46),
    node("公開URLが閉じる", "誰が開いても 403", RED, RED_S, 250), arrow("", 46),
    node("元に戻す", "翌月にスイッチと<br>公開設定を戻す", GREEN, GREEN_S, 250),
    gap=10, align="center")
slides["flow-limit"] = page("flow-limit", "上限に近づいたとき", "上限の手前で、キャラが自分から会話を終える", col(
    h3("ふだんの止まり方(すぐ止まる)", 32, SUB), meter, say,
    row(h3("最後の保険(数時間遅れ)", 32, SUB), pill("実際に試して確認済み", GREEN, GREEN_S, 20), gap=16, align="center",
        style="margin-top:22px"), kill_flow,
    f'<div style="background:{NAVY};border-radius:20px;padding:20px 30px;display:flex;flex-direction:row;align-items:center;gap:18px;margin-top:14px">'
    f'{icon("Chart", "#F2B27A", 36)}<p style="font-size:24px;color:#E6EBF5">実測では 4往復で約0.02ドル。1日1ドルなら、上限に届くのは約40分話したあと。</p></div>',
    gap=22), gap=30)


# ---------------------------------------------------------------- 長く話す工夫
def cost_chart():
    # 何もしない場合(履歴が増え続ける)と、圧縮した場合(一定で止まる)の、1往復あたりの費用のイメージ
    w, h = 620, 260
    pts_a = " ".join(f"{40 + i * 56},{h - 30 - i * 19}" for i in range(11))
    pts_b = " ".join(f"{40 + i * 56},{h - 30 - min(i, 4) * 19}" for i in range(11))
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<line x1="40" y1="{h - 30}" x2="{w - 10}" y2="{h - 30}" stroke="{LINE}" stroke-width="3"/>'
            f'<line x1="40" y1="20" x2="40" y2="{h - 30}" stroke="{LINE}" stroke-width="3"/>'
            f'<polyline points="{pts_a}" fill="none" stroke="{RED}" stroke-width="5" stroke-dasharray="12 8"/>'
            f'<polyline points="{pts_b}" fill="none" stroke="{GREEN}" stroke-width="6"/>'
            f'<text x="{w - 170}" y="34" font-size="22" fill="{RED}" font-family="Noto Sans JP">圧縮しない</text>'
            f'<text x="{w - 170}" y="{h - 120}" font-size="22" fill="{GREEN}" font-family="Noto Sans JP" font-weight="700">圧縮する</text>'
            f'<text x="44" y="{h - 4}" font-size="20" fill="{SUB}" font-family="Noto Sans JP">会話の往復 →</text>'
            f'<text x="0" y="16" font-size="20" fill="{SUB}" font-family="Noto Sans JP">1往復の費用</text></svg>')


tips = row(
    card(row(badge("Link", BLUE, "#E1ECFA", 64), h3("切れても続く", 32), gap=14, align="center") +
         p("Gemini との接続は約10分で切れる。切れる前に届く合図を受けて、自動でつなぎ直す。", 24, SUB) +
         col(*[row(f'<p style="{HEAD};font-size:28px;color:{BLUE};width:34px">{n}</p>', p(t, 24), gap=10, align="center",
                   style="background:#EEF3FB;border-radius:14px;padding:10px 16px")
               for n, t in [("1", "会話している"), ("2", "合図(goAway)が届く"), ("3", "合言葉で、つなぎ直す"), ("4", "会話は続きから")]], gap=8),
         top=BLUE),
    card(row(badge("Chart", GREEN, GREEN_S, 64), h3("履歴を小さく保つ", 32), gap=14, align="center") +
         p("Gemini は毎回、それまでの会話も読み直して課金される。12,000トークンを超えたら古い部分を切り、6,000トークンまで縮める。", 24, SUB) +
         f'<div style="align-items:center">{cost_chart()}</div>', top=GREEN, style="flex:1.4"),
    card(row(badge("Clock", ACCENT, WARM, 64), h3("無音は送らない", 32), gap=14, align="center") +
         p("話していない時間の音は送らないので、課金されない。考えている間や聞いている間は0円。", 24, SUB) +
         '<svg width="420" height="150" viewBox="0 0 420 150">'
         + "".join(f'<rect x="{x}" y="40" width="{w}" height="50" rx="10" fill="{c}"/>' for x, w, c in
                   [(0, 70, "#ECEAE4"), (70, 110, ACCENT), (180, 90, "#ECEAE4"), (270, 80, ACCENT), (350, 70, "#ECEAE4")])
         + f'<text x="100" y="125" font-size="22" fill="{ACCENT}" font-family="Noto Sans JP" font-weight="700">送る</text>'
         + f'<text x="286" y="125" font-size="22" fill="{ACCENT}" font-family="Noto Sans JP" font-weight="700">送る</text>'
         + f'<text x="0" y="26" font-size="20" fill="{SUB}" font-family="Noto Sans JP">マイクの音 →</text></svg>',
         top=ACCENT),
    gap=24)
slides["flow-session"] = page("flow-session", "長く話す工夫", "長く話しても、途切れず、費用も増え続けない", tips, gap=36)

# ---------------------------------------------------------------- 書き出し
order = ["cover-arch", "arch-overview", "arch-why", "arch-gcp", "arch-browser", "arch-cost",
         "cover-flow", "flow-turn", "flow-interrupt", "flow-tools", "flow-persona", "flow-limit", "flow-session"]
for sid in order:
    (OUT / f"{sid}.html").write_text(slides[sid], encoding="utf-8")
(OUT / "decks.json").write_text(
    '{"architecture": ' + str(order[:6]).replace("'", '"') + ', "flow": ' + str(order[6:]).replace("'", '"') + "}\n",
    encoding="utf-8")
print(len(order), "slides ->", OUT)
