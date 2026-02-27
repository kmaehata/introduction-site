# AWS セットアップガイド

## 全体の流れ

```
Step 1  Bedrock でモデルを有効化
Step 2  S3 バケットを2つ作成
Step 3  Lambda 関数を作成
Step 4  Lambda Function URL を有効化
Step 5  CloudFront ディストリビューションを作成
Step 6  S3 バケットポリシーを設定
Step 7  IAM ユーザー (GitHub Actions 用) を作成
Step 8  GitHub Secrets を設定
Step 9  知識ベースを初期化 (ローカルで1回だけ実行)
Step 10 GitHub に push → 自動デプロイ確認
```

---

## Step 1 — Bedrock でモデルを有効化(廃止されているのでこのステップは飛ばしOK)

1. AWS Console → **Amazon Bedrock** → **Model access**
2. リージョンを **ap-northeast-1 (東京)** に切り替え
3. 「**Manage model access**」をクリック
4. 以下2つにチェックを入れて「**Save changes**」
   - ✅ `Amazon Titan Text Embeddings V2`
   - ✅ `Anthropic Claude 3 Haiku`
5. Status が **Access granted** になるまで待つ（数分）

---

## Step 2 — S3 バケットを2つ作成

### バケット A: ウェブサイト用

1. AWS Console → **S3** → 「**バケットを作成**」
2. 設定:
   - バケット名: `kosei-portfolio-site`（任意、グローバルユニーク）
   - リージョン: `ap-northeast-1`
   - **パブリックアクセスをすべてブロック: オン**（CloudFront OAC で配信するため）
   - 他はデフォルト → 「作成」

### バケット B: 知識ベース用

1. 「**バケットを作成**」
2. 設定:
   - バケット名: `kosei-portfolio-kb`（任意）
   - リージョン: `ap-northeast-1`
   - パブリックアクセスをすべてブロック: オン
   - 他はデフォルト → 「作成」

---

## Step 3 — Lambda 関数を作成

1. AWS Console → **Lambda** → 「**関数の作成**」
2. 設定:
   - 関数名: `kosei-portfolio-rag`
   - ランタイム: **Python 3.12**
   - アーキテクチャ: `x86_64`
   - 「**関数の作成**」をクリック

### 実行ロールに権限を付与

1. 作成した関数 → **設定** タブ → **アクセス権限** → ロール名をクリック
2. IAM コンソールが開く → 「**インラインポリシーを追加**」
3. JSON タブに `aws/infrastructure/lambda_policy.json` の内容を貼り付け
   - `YOUR_KB_BUCKET_NAME` を `kosei-portfolio-kb` に置換
4. ポリシー名: `KoseiPortfolioLambdaPolicy` → 「保存」

### 環境変数を設定

1. Lambda → **設定** タブ → **環境変数** → 「**編集**」
2. 追加:
   - キー: `EMBEDDINGS_BUCKET`、値: `kosei-portfolio-kb`
   - キー: `BEDROCK_REGION`、値: `ap-northeast-1`
3. 保存

### タイムアウトとメモリを変更

1. **設定** タブ → **一般設定** → 「**編集**」
2. タイムアウト: `0分 30秒`
3. メモリ: `512 MB`
4. 保存

---

## Step 4 — Lambda Function URL を有効化

1. Lambda → **設定** タブ → **関数 URL** → 「**作成**」
2. 設定:
   - 認証タイプ: **NONE**（パブリックアクセス）
   - CORS を設定: **オン**
3. CORS 設定:
   - 許可オリジン: `*`
   - 許可メソッド: `POST`、`OPTIONS` (両方チェック)
   - 許可ヘッダー: `content-type`
4. 「保存」

**Function URL をコピーしておく**（例: `https://xxxxxxxx.lambda-url.ap-northeast-1.on.aws/`）

---

## Step 5 — CloudFront ディストリビューションを作成

### 5-1. CloudFront Function を作成（URL リライト用）

1. AWS Console → **CloudFront** → **Functions** → 「**関数を作成**」
2. 名前: `portfolio-url-rewrite`
3. ランタイム: `cloudfront-js-2.0`
4. 「**作成**」後、エディタに `aws/infrastructure/cf_function.js` の内容を貼り付け
5. 「**保存**」→ 「**発行**」

### 5-2. ディストリビューションを作成

1. **CloudFront** → 「**ディストリビューションを作成**」
2. オリジン設定:
   - オリジンドメイン: S3 バケット `kosei-portfolio-site` を選択
   - オリジンアクセス: **Origin access control settings (OAC)** を選択
   - 「**新しい OAC を作成**」→ デフォルトで「**作成**」
3. デフォルトキャッシュビヘイビアー:
   - ビューワープロトコルポリシー: **Redirect HTTP to HTTPS**
   - キャッシュポリシー: **CachingOptimized**
4. 関数の関連付け:
   - ビューワーリクエスト → 「**CloudFront Functions**」→ `portfolio-url-rewrite`
5. 設定:
   - デフォルトルートオブジェクト: `index.html`
   - カスタムエラーレスポンス: 404 → `/index.html`、HTTP 200 で返す
6. 「**ディストリビューションを作成**」

**ディストリビューション ID とドメイン名をコピー**

### 5-3. S3 バケットポリシーを設定

CloudFront 作成後、コンソールに「バケットポリシーをコピー」バナーが表示されるので:
1. 「**ポリシーをコピー**」
2. S3 → `kosei-portfolio-site` → **アクセス許可** → **バケットポリシー** → 「**編集**」
3. コピーしたポリシーを貼り付け → 「保存」

---

## Step 6 — IAM ユーザー (GitHub Actions 用) を作成

1. IAM → **ユーザー** → 「**ユーザーを作成**」
2. ユーザー名: `github-actions-portfolio`
3. 「**次へ**」→「**ポリシーを直接アタッチ**」→「**インラインポリシーを作成**」
4. JSON タブに `aws/infrastructure/github_actions_policy.json` の内容を貼り付け
   - `YOUR_WEBSITE_BUCKET_NAME` → `kosei-portfolio-site`
   - `YOUR_ACCOUNT_ID` → AWS アカウント ID（12桁）
   - `YOUR_DISTRIBUTION_ID` → Step 5 でコピーした Distribution ID
   - `YOUR_LAMBDA_FUNCTION_NAME` → `kosei-portfolio-rag`
5. 「**ユーザーを作成**」

### アクセスキーを発行

1. 作成したユーザー → **セキュリティ認証情報** タブ
2. 「**アクセスキーを作成**」→ **CLI 用** を選択
3. **アクセスキー ID** と **シークレットアクセスキー** をコピー（後で使用）

---

## Step 7 — GitHub Secrets を設定

GitHub リポジトリ → **Settings** → **Secrets and variables** → **Actions** → 「**New repository secret**」

| シークレット名 | 値 |
|---|---|
| `AWS_ACCESS_KEY_ID` | Step 6 のアクセスキー ID |
| `AWS_SECRET_ACCESS_KEY` | Step 6 のシークレットアクセスキー |
| `AWS_REGION` | `ap-northeast-1` |
| `S3_BUCKET` | `kosei-portfolio-site` |
| `CF_DISTRIBUTION_ID` | CloudFront Distribution ID |
| `LAMBDA_FUNCTION_NAME` | `kosei-portfolio-rag` |
| `AI_API_URL` | Lambda Function URL（Step 4 でコピーしたもの） |

---

## Step 8 — 知識ベースを初期化（ローカルで1回実行）

```bash
cd aws/scripts

# 依存パッケージをインストール
pip install -r requirements.txt

# AWS 認証情報を設定（未設定の場合）
aws configure

# PDF を読み込んでエンベディングを生成・S3 アップロード
python prepare_embeddings.py --bucket kosei-portfolio-kb --region ap-northeast-1

# 確認（S3 にファイルが存在するか）
aws s3 ls s3://kosei-portfolio-kb/
```

成功すると `knowledge_base.json` が S3 にアップロードされます。

---

## Step 9 — デプロイ実行

```bash
git add .
git commit -m "feat: add AI chat backend"
git push origin main
```

GitHub Actions が自動的に:
1. Next.js をビルド（static export）
2. S3 に同期
3. CloudFront キャッシュを削除
4. Lambda を更新

**GitHub → Actions タブでログを確認できます。**

---

## 動作確認

1. CloudFront ドメイン（例: `https://d1abc123.cloudfront.net`）にアクセス
2. TOP ページのチャット欄にメッセージを入力
3. キャラクターが thinking → talking → stand と切り替わり、AI が回答すれば完成 🎉

---

## コスト試算（月額）

| サービス | 条件 | 料金 |
|---|---|---|
| S3 | 100MB, 10K リクエスト | ~$0.01 |
| CloudFront | 1GB 転送, 100K リクエスト | ~$0.10 |
| Lambda | 500回 × 3秒 × 512MB | **無料枠内** |
| Bedrock Titan Embeddings V2 | クエリ埋め込み 500回 | ~$0.01 |
| Bedrock Claude 3 Haiku | 500クエリ × 500トークン | ~$0.20 |
| **合計** | | **< $0.50/月** |

---

## トラブルシューティング

### Lambda で "AccessDenied"
→ IAM ロールに Bedrock と S3 の権限が付与されているか確認

### 「knowledge_base.json が見つからない」
→ Step 8 の `prepare_embeddings.py` を実行したか確認

### CloudFront で 403/404
→ S3 バケットポリシーが正しく設定されているか確認（Step 5-3）

### チャットが mock のまま
→ GitHub Secret `AI_API_URL` が正しく設定されているか確認
→ Lambda Function URL を直接 curl でテスト:
```bash
curl -X POST https://YOUR_FUNCTION_URL \
  -H "Content-Type: application/json" \
  -d '{"query": "あなたは何が得意ですか？"}'
```
