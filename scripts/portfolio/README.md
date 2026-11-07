# ポートフォリオの資料を追加する手順

作品ページ(`/portfolio/<slug>/`)は `data/portfolio/index.ts` だけを見て作られます。
新しい版を出すときは、資料を書き出して置き、データに1件足すだけです。

## 1. 資料を画像と PDF に書き出す

スライドの HTML(1枚1ファイル、`<section>` 1つ)を1つのフォルダに置いて実行します。
Playwright と Chromium が必要です。

```bash
node scripts/portfolio/make-covers.js <スライドのフォルダ>
```

```bash
node scripts/portfolio/export-slides.js <スライドのフォルダ> <出力先>
```

- 冊子の組み合わせは `export-slides.js` の `decks` で決めます。
- 表紙の目次と版の表記は `make-covers.js` で決めます。
- 出力先には、冊子ごとの `01.jpg…`、`<冊子>.pdf`、目次の `manifest.json` ができます。

## 2. サイトに置く

- 画像と PDF: `public/portfolio/<slug>/v<版>/`
- 目次: `data/portfolio/<slug>-v<版>.json`(`manifest.json` を名前を変えて置く)

## 3. データに版を足す

`data/portfolio/index.ts` の `versions` の**先頭**に1件足します(新しい版が先頭)。

- `version` / `date` / `title`: 版の番号・日付・ひとこと
- `highlights`: その版の見どころ(画面の「v○○」の下に並ぶ)
- `docs`: 資料。`audience` に `engineer` / `business` を入れると、画面の絞り込みに出ます

古い版も残るので、画面の「VERSIONS」から切り替えて読めます。
`/portfolio/<slug>/#v1.0` のように、版を指定したリンクも作れます。
