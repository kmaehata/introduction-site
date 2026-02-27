# ポートフォリオサイト

自己紹介・経歴紹介のためのコーポレーションサイト風ポートフォリオサイトです。

## 技術スタック

### フロントエンド
- **Next.js 14** (React)
- **TypeScript**
- **CSS Modules**

### バックエンド
- **Python**
- **FastAPI**
- **Uvicorn**

## 機能

5つのタブで構成されたシングルページアプリケーション:

1. **大学卒業研究** - Deep Q-Learningを用いた経路最適化研究
2. **AIモデルの開発** - 画像分類モデルの研究開発経験
3. **IT戦士(クラウド系)** - フルスタックエンジニアとしての経験
4. **生成AIの強いエンジニア** - 生成AI・チャットbot開発経験
5. **ポートフォリオ一覧** - 制作物・実績一覧(準備中)

## セットアップ

### フロントエンド(Next.js)

1. 依存パッケージのインストール:
```bash
npm install
```

2. 開発サーバーの起動:
```bash
npm run dev
```

3. ブラウザで http://localhost:3000 にアクセス

### バックエンド(Python/FastAPI)

1. バックエンドディレクトリに移動:
```bash
cd backend
```

2. 仮想環境の作成と有効化:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. 依存パッケージのインストール:
```bash
pip install -r requirements.txt
```

4. サーバーの起動:
```bash
python main.py
```

5. APIドキュメント: http://localhost:8000/docs

## プロジェクト構造

```
introduction-site/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # ルートレイアウト
│   ├── page.tsx           # メインページ
│   ├── page.module.css    # ページスタイル
│   └── globals.css        # グローバルスタイル
├── components/            # Reactコンポーネント
│   ├── UniversityResearch.tsx      # 大学研究タブ
│   ├── AIModelDevelopment.tsx      # AIモデル開発タブ
│   ├── CloudEngineer.tsx           # クラウドエンジニアタブ
│   ├── GenerativeAI.tsx            # 生成AIタブ
│   ├── PortfolioList.tsx           # ポートフォリオ一覧タブ
│   └── TabContent.module.css       # タブコンテンツスタイル
├── backend/               # Pythonバックエンド
│   ├── main.py           # FastAPIアプリケーション
│   ├── requirements.txt  # Python依存パッケージ
│   └── README.md         # バックエンドREADME
├── package.json          # Node.js依存関係
├── tsconfig.json         # TypeScript設定
├── next.config.js        # Next.js設定
└── README.md            # このファイル
```

## 開発

### フロントエンドの開発

```bash
npm run dev    # 開発サーバー起動
npm run build  # 本番ビルド
npm run start  # 本番サーバー起動
npm run lint   # リント実行
```

### バックエンドの開発

```bash
# 開発モード(自動リロード有効)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 今後の拡張予定

- [ ] ポートフォリオ一覧の実装
- [ ] お問い合わせフォーム
- [ ] ダークモード対応
- [ ] アニメーション強化
- [ ] レスポンシブデザインの最適化
- [ ] データベース連携(PostgreSQL/MongoDB)
- [ ] 管理画面の追加

## ライセンス

Private
