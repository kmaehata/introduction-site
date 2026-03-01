"""
Portfolio AI Chat — Lambda RAG Handler
--------------------------------------
Flow:
  1. Load pre-computed embeddings from S3 (cached in execution context)
  2. Embed user query via Bedrock Titan Embeddings V2
  3. Cosine similarity search (numpy, no vector DB needed)
  4. Generate answer via Claude 3 Haiku with retrieved context
  5. Return JSON response
"""

import json
import os
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
LLM_MODEL = "anthropic.claude-3-haiku-20240307-v1:0"
EMBED_DIMENSIONS = 256
TOP_K = 4
MAX_TOKENS = 220

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


def embed(text: str) -> np.ndarray:
    resp = bedrock.invoke_model(
        modelId=EMBED_MODEL,
        body=json.dumps({
            "inputText": text,
            "dimensions": EMBED_DIMENSIONS,
            "normalize": True,
        }),
    )
    vec = json.loads(resp["body"].read())["embedding"]
    return np.array(vec, dtype=np.float32)


def retrieve(query: str, top_k: int = TOP_K) -> list[str]:
    kb = load_kb()
    if len(kb["texts"]) == 0:
        return []
    q_emb = embed(query)
    # Dot product = cosine similarity (embeddings are L2-normalized by Titan)
    scores = kb["embeddings"] @ q_emb
    top_idx = np.argsort(scores)[::-1][:top_k]
    return [kb["texts"][i] for i in top_idx]


def generate(query: str, context_chunks: list[str]) -> str:
    if context_chunks:
        context = "\n\n---\n\n".join(context_chunks)
    else:
        context = ""

    system_prompt = f"""あなたは前畑康成（28歳、Cloud & AI Engineer）本人です。
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
    return result["content"][0]["text"]


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

        chunks = retrieve(query)
        answer = generate(query, chunks)
        return ok({"response": answer})

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return err(500, "システムエラーが発生しました。しばらくしてからお試しください。")
