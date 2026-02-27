#!/usr/bin/env python3
"""
PDF → チャンク → Bedrock Titan Embedding → S3 アップロード

事前に1回だけ実行する知識ベース構築スクリプト。

使い方:
    pip install -r requirements.txt
    python prepare_embeddings.py --bucket YOUR_KB_BUCKET

オプション:
    --bucket    S3 バケット名 (必須)
    --region    AWS リージョン (デフォルト: ap-northeast-1)
    --pdf       PDF ファイルパス (デフォルト: ../data/職務経歴書km20251225.pdf)
    --scenario  シナリオファイルパス (デフォルト: ../data/sinario.txt)
    --dry-run   S3 アップロードをスキップして確認のみ
"""

import argparse
import json
import os
import re
import sys

import boto3
import pdfplumber

# ── Text extraction ───────────────────────────────────────────────────────────

def extract_pdf(pdf_path: str) -> list[str]:
    """PDF の各ページからテキストを抽出する"""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            text = text.strip()
            if text:
                pages.append(f"[Page {i + 1}]\n{text}")
    return pages


def extract_scenario(scenario_path: str) -> list[str]:
    """シナリオファイルから Q&A ペアを抽出する"""
    with open(scenario_path, encoding="utf-8") as f:
        content = f.read()

    chunks = []
    # "シナリオN" → Q → A の繰り返しを解析
    blocks = re.split(r"シナリオ\d+", content)
    for block in blocks:
        qa_parts = re.split(r"\nQ\n", block)
        for qa in qa_parts[1:]:  # 最初の空要素をスキップ
            parts = re.split(r"\nA\n", qa)
            if len(parts) == 2:
                q = parts[0].strip()
                a = parts[1].strip()
                chunks.append(f"Q: {q}\nA: {a}")
    return chunks


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_pages(pages: list[str], max_chars: int = 700, overlap: int = 80) -> list[str]:
    """ページテキストをオーバーラップ付きでチャンク分割する"""
    chunks = []
    for page_text in pages:
        lines = page_text.split("\n")
        current = ""
        for line in lines:
            if len(current) + len(line) + 1 > max_chars and current:
                chunks.append(current.strip())
                current = current[-overlap:] + "\n" + line
            else:
                current += "\n" + line if current else line
        if current.strip():
            chunks.append(current.strip())
    return chunks


# ── Embedding ─────────────────────────────────────────────────────────────────

def embed(bedrock_client, text: str, dimensions: int = 256) -> list[float]:
    resp = bedrock_client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({
            "inputText": text,
            "dimensions": dimensions,
            "normalize": True,
        }),
    )
    return json.loads(resp["body"].read())["embedding"]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ナレッジベースを構築して S3 にアップロードします")
    parser.add_argument("--bucket", required=True, help="S3 バケット名")
    parser.add_argument("--region", default="ap-northeast-1")
    parser.add_argument("--pdf", default="../data/職務経歴書km20251225.pdf")
    parser.add_argument("--scenario", default="../data/sinario.txt")
    parser.add_argument("--dimensions", type=int, default=256)
    parser.add_argument("--dry-run", action="store_true", help="S3 アップロードをスキップ")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, args.pdf)
    scenario_path = os.path.join(script_dir, args.scenario)

    if not os.path.exists(pdf_path):
        print(f"❌ PDF が見つかりません: {pdf_path}")
        sys.exit(1)

    bedrock = boto3.client("bedrock-runtime", region_name=args.region)
    s3 = boto3.client("s3", region_name=args.region)

    # 1. テキスト抽出
    print("📄 PDF からテキスト抽出中...")
    pages = extract_pdf(pdf_path)
    print(f"   {len(pages)} ページ抽出完了")

    # 2. チャンク分割
    print("✂️  チャンク分割中...")
    chunks = chunk_pages(pages)
    print(f"   PDF から {len(chunks)} チャンク生成")

    # 3. シナリオ Q&A 追加
    if os.path.exists(scenario_path):
        print("💬 シナリオ Q&A を追加中...")
        qa_chunks = extract_scenario(scenario_path)
        chunks.extend(qa_chunks)
        print(f"   {len(qa_chunks)} Q&A ペア追加 → 合計 {len(chunks)} チャンク")

    # 4. エンベディング生成
    print(f"\n🔢 エンベディング生成中 ({args.dimensions}次元) ...")
    knowledge_base = {"chunks": [], "dimensions": args.dimensions}
    errors = 0

    for i, chunk in enumerate(chunks):
        preview = chunk[:60].replace("\n", " ")
        print(f"   [{i + 1:3d}/{len(chunks)}] {preview}...", end=" ")
        try:
            vec = embed(bedrock, chunk, args.dimensions)
            knowledge_base["chunks"].append({"text": chunk, "embedding": vec})
            print("✓")
        except Exception as e:
            print(f"⚠️  スキップ ({e})")
            errors += 1

    if errors:
        print(f"\n⚠️  {errors} チャンクをスキップしました")

    # 5. S3 アップロード
    kb_json = json.dumps(knowledge_base, ensure_ascii=False).encode("utf-8")
    print(f"\n📦 ナレッジベースサイズ: {len(kb_json) / 1024:.1f} KB")

    if args.dry_run:
        print("🔍 --dry-run モード: S3 アップロードをスキップしました")
        return

    print(f"☁️  S3 にアップロード中... (s3://{args.bucket}/knowledge_base.json)")
    s3.put_object(
        Bucket=args.bucket,
        Key="knowledge_base.json",
        Body=kb_json,
        ContentType="application/json; charset=utf-8",
    )
    print(f"✅ 完了！ {len(knowledge_base['chunks'])} チャンクをアップロードしました")
    print(f"   次のステップ: Lambda の環境変数 EMBEDDINGS_BUCKET に '{args.bucket}' を設定してください")


if __name__ == "__main__":
    main()
