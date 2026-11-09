"""
Portfolio AI Chat — Lambda RAG Handler
--------------------------------------
流れ:
  1. 今月の利用額を確かめ、上限(既定 3 USD)を超えそうなら答えずに断る
  2. 事前に作った埋め込みを S3 から読む(実行環境が温かい間は使い回す)
  3. 質問を Bedrock Titan Embeddings V2 で埋め込みにする
  4. コサイン類似度で近い経歴の文を探す(numpy、ベクトル DB は使わない)
  5. Claude Sonnet で答えを作り、使ったトークンから費用を計算して今月の利用額に足す
"""

import json
import os
from datetime import datetime, timedelta, timezone

import boto3
import numpy as np

# ── AWS clients (reused across warm invocations) ─────────────────────────────
REGION = os.environ.get("BEDROCK_REGION", "ap-northeast-1")
bedrock = boto3.client("bedrock-runtime", region_name=REGION)
s3 = boto3.client("s3")

# ── Config ────────────────────────────────────────────────────────────────────
EMBEDDINGS_BUCKET = os.environ["EMBEDDINGS_BUCKET"]
EMBEDDINGS_KEY = "knowledge_base.json"
EMBED_MODEL = "amazon.titan-embed-text-v2:0"
# このアカウントで使える最新の Sonnet(日本国内で処理する推論プロファイル)。Sonnet 5 系はまだ使えない
LLM_MODEL = os.environ.get("LLM_MODEL", "jp.anthropic.claude-sonnet-4-6")
EMBED_DIMENSIONS = 256
TOP_K = 4
MAX_TOKENS = 220

# ── 月の上限 ──────────────────────────────────────────────────────────────────
# 料金は 100万トークンあたりの USD。Sonnet 4.6 の単価に、日本国内で処理する分の上乗せ(1割)を見込んだ値。
# モデルを変えたら環境変数で合わせる
MONTHLY_BUDGET_USD = float(os.environ.get("MONTHLY_BUDGET_USD", "3"))
PRICE_INPUT_PER_MTOK = float(os.environ.get("PRICE_INPUT_PER_MTOK", "3.3"))
PRICE_OUTPUT_PER_MTOK = float(os.environ.get("PRICE_OUTPUT_PER_MTOK", "16.5"))
PRICE_EMBED_PER_MTOK = float(os.environ.get("PRICE_EMBED_PER_MTOK", "0.02"))
USAGE_PREFIX = "usage/"
JST = timezone(timedelta(hours=9))
LIMIT_MESSAGE = "今月はたくさん質問をいただいたので、チャットはお休みしています。来月またお試しください。"

# ── Knowledge base cache (persists across warm invocations) ──────────────────
_kb: dict | None = None


def load_kb() -> dict:
    global _kb
    if _kb is not None:
        return _kb
    try:
        obj = s3.get_object(Bucket=EMBEDDINGS_BUCKET, Key=EMBEDDINGS_KEY)
        raw = json.loads(obj["Body"].read().decode("utf-8"))
        texts = [c["text"] for c in raw["chunks"]]
        embs = np.array([c["embedding"] for c in raw["chunks"]], dtype=np.float32)
        _kb = {"texts": texts, "embeddings": embs}
        print(f"[KB] Loaded {len(texts)} chunks")
    except Exception as e:
        print(f"[KB] Failed to load: {e}")
        _kb = {"texts": [], "embeddings": np.empty((0, EMBED_DIMENSIONS), dtype=np.float32)}
    return _kb


def embed(text: str) -> tuple[np.ndarray, int]:
    resp = bedrock.invoke_model(
        modelId=EMBED_MODEL,
        body=json.dumps({
            "inputText": text,
            "dimensions": EMBED_DIMENSIONS,
            "normalize": True,
        }),
    )
    data = json.loads(resp["body"].read())
    return np.array(data["embedding"], dtype=np.float32), int(data.get("inputTextTokenCount", 0))


def retrieve(query: str, top_k: int = TOP_K) -> tuple[list[str], int]:
    """近い文と、埋め込みに使ったトークン数を返す"""
    kb = load_kb()
    if len(kb["texts"]) == 0:
        return [], 0
    q_emb, tokens = embed(query)
    # Dot product = cosine similarity (embeddings are L2-normalized by Titan)
    scores = kb["embeddings"] @ q_emb
    top_idx = np.argsort(scores)[::-1][:top_k]
    return [kb["texts"][i] for i in top_idx], tokens


def generate(query: str, context_chunks: list[str]) -> tuple[str, dict]:
    if context_chunks:
        context = "\n\n---\n\n".join(context_chunks)
    else:
        context = ""

    system_prompt = f"""あなたはK.M（29歳、Cloud & AI Engineer）本人です。名前を聞かれたら「K.M」と答え、本名は答えないでください。
ポートフォリオサイトを訪れた方とチャットで話しています。

【自分のこと】
{context if context else "（一般的な会話には経歴情報なしで自然に対応してください）"}

【話し方】
- 一人称は「私」、ていねい語だが硬くなりすぎない自然なトーン
- 1〜2文で答える。長々と説明しない。箇条書きは絶対使わない
- 挨拶・雑談には軽く乗る
- 技術・経歴について聞かれたら上の情報をもとに具体的かつ簡潔に答える
- わからないことは「詳しくはお問い合わせいただけると嬉しいです」と一言で"""

    resp = bedrock.invoke_model(
        modelId=LLM_MODEL,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": MAX_TOKENS,
            "temperature": 0.85,
            "system": system_prompt,
            "messages": [{"role": "user", "content": query}],
        }),
    )
    result = json.loads(resp["body"].read())
    text = "".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")
    return text, result.get("usage", {})


# ── 月の利用額(S3 に月ごとの JSON で記録する) ───────────────────────────────
def usage_key(now: datetime | None = None) -> str:
    now = now or datetime.now(JST)
    return f"{USAGE_PREFIX}{now:%Y-%m}.json"


def load_usage(key: str) -> dict:
    try:
        obj = s3.get_object(Bucket=EMBEDDINGS_BUCKET, Key=key)
        return json.loads(obj["Body"].read())
    except s3.exceptions.NoSuchKey:
        return {"cost_usd": 0.0, "chats": 0, "input_tokens": 0, "output_tokens": 0, "embed_tokens": 0}


def save_usage(key: str, usage: dict) -> None:
    s3.put_object(Bucket=EMBEDDINGS_BUCKET, Key=key, ContentType="application/json",
                  Body=json.dumps(usage, ensure_ascii=False).encode("utf-8"))


def chat_cost(llm_usage: dict, embed_tokens: int) -> float:
    return (llm_usage.get("input_tokens", 0) * PRICE_INPUT_PER_MTOK
            + llm_usage.get("output_tokens", 0) * PRICE_OUTPUT_PER_MTOK
            + embed_tokens * PRICE_EMBED_PER_MTOK) / 1_000_000


def worst_case_cost(query: str) -> float:
    """1回の質問で最大どれだけかかるかの見積もり(多めに見る)"""
    input_tokens = 2_500 + len(query) * 2  # システムプロンプトと経歴の文 + 質問
    return (input_tokens * PRICE_INPUT_PER_MTOK + MAX_TOKENS * PRICE_OUTPUT_PER_MTOK) / 1_000_000


# ── Helpers ───────────────────────────────────────────────────────────────────
HEADERS = {"Content-Type": "application/json"}


def ok(body: dict) -> dict:
    return {"statusCode": 200, "headers": HEADERS, "body": json.dumps(body, ensure_ascii=False)}


def err(code: int, msg: str) -> dict:
    return {"statusCode": code, "headers": HEADERS, "body": json.dumps({"error": msg}, ensure_ascii=False)}


# ── Handler ───────────────────────────────────────────────────────────────────
def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "POST")

    # CORS preflight は Function URL 側で処理
    if method == "OPTIONS":
        return {"statusCode": 200, "headers": HEADERS, "body": ""}

    if method != "POST":
        return err(405, "Method Not Allowed")

    try:
        body = json.loads(event.get("body") or "{}")
        query = (body.get("query") or "").strip()
        if not query:
            return err(400, "query フィールドが必要です")

        if len(query) > 500:
            return err(400, "質問は500文字までにしてください")

        # 今月の利用額が上限を超えそうなら、モデルを呼ばずに断る
        key = usage_key()
        usage = load_usage(key)
        if usage["cost_usd"] + worst_case_cost(query) > MONTHLY_BUDGET_USD:
            print(f"[BUDGET] 上限に達したため回答しない: {usage['cost_usd']:.4f} USD")
            return ok({"response": LIMIT_MESSAGE, "limited": True})

        chunks, embed_tokens = retrieve(query)
        answer, llm_usage = generate(query, chunks)

        cost = chat_cost(llm_usage, embed_tokens)
        usage = load_usage(key)  # 生成の間に他の人が使った分を取りこぼさないよう、読み直して足す
        usage["cost_usd"] = round(usage["cost_usd"] + cost, 6)
        usage["chats"] += 1
        usage["input_tokens"] += llm_usage.get("input_tokens", 0)
        usage["output_tokens"] += llm_usage.get("output_tokens", 0)
        usage["embed_tokens"] += embed_tokens
        try:
            save_usage(key, usage)
        except Exception as e:  # 記録に失敗しても、答えは返す
            print(f"[BUDGET] 利用額の記録に失敗: {e}")
        print(f"[BUDGET] 今回 {cost:.5f} USD / 今月 {usage['cost_usd']:.4f} USD / {usage['chats']} 回")
        return ok({"response": answer})

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return err(500, "システムエラーが発生しました。しばらくしてからお試しください。")
