# Backend README

## セットアップ

### 仮想環境の作成
```bash
python -m venv venv
```

### 仮想環境の有効化
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

## サーバーの起動

```bash
python main.py
```

または

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## APIドキュメント

サーバー起動後、以下のURLでSwagger UIにアクセスできます:
- http://localhost:8000/docs

## エンドポイント

- `GET /` - API情報
- `GET /api/portfolios` - ポートフォリオ一覧取得
- `GET /api/portfolios/{id}` - 特定ポートフォリオ取得
- `GET /api/experiences` - 経歴一覧取得
- `POST /api/portfolios` - ポートフォリオ追加
