from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="ポートフォリオAPI",
    description="ポートフォリオサイト用のバックエンドAPI",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.jsの開発サーバー
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# データモデル定義
class Portfolio(BaseModel):
    id: int
    title: str
    description: str
    technologies: List[str]
    url: str | None = None
    github_url: str | None = None


class Experience(BaseModel):
    id: int
    company: str
    role: str
    period: str
    description: str


# サンプルデータ
portfolios = [
    {
        "id": 1,
        "title": "サンプルプロジェクト1",
        "description": "生成AIを活用したチャットボット",
        "technologies": ["Python", "FastAPI", "OpenAI API", "React"],
        "url": None,
        "github_url": None
    }
]

experiences = [
    {
        "id": 1,
        "company": "ニューロンネットワーク株式会社",
        "role": "AIモデル開発(アルバイト)",
        "period": "2020-2021",
        "description": "マルチ画像分類モデルの研究・開発"
    },
    {
        "id": 2,
        "company": "Kyla株式会社",
        "role": "フルスタックエンジニア",
        "period": "2021-2022",
        "description": "クラウド環境でのバックエンド・インフラ・Web開発"
    },
    {
        "id": 3,
        "company": "AIタレントフォース株式会社",
        "role": "生成AIエンジニア",
        "period": "2022-2024",
        "description": "生成AIプロジェクト、チャットbot開発"
    },
    {
        "id": 4,
        "company": "フリーランス",
        "role": "フルスタックエンジニア",
        "period": "2024-現在",
        "description": "生成AI技術を活用したソリューション開発"
    }
]


@app.get("/")
async def root():
    return {
        "message": "ポートフォリオAPI",
        "version": "1.0.0",
        "endpoints": [
            "/api/portfolios",
            "/api/experiences"
        ]
    }


@app.get("/api/portfolios", response_model=List[Portfolio])
async def get_portfolios():
    """ポートフォリオ一覧を取得"""
    return portfolios


@app.get("/api/portfolios/{portfolio_id}", response_model=Portfolio)
async def get_portfolio(portfolio_id: int):
    """特定のポートフォリオを取得"""
    for portfolio in portfolios:
        if portfolio["id"] == portfolio_id:
            return portfolio
    return {"error": "Portfolio not found"}


@app.get("/api/experiences", response_model=List[Experience])
async def get_experiences():
    """経歴一覧を取得"""
    return experiences


@app.post("/api/portfolios", response_model=Portfolio)
async def create_portfolio(portfolio: Portfolio):
    """新しいポートフォリオを追加"""
    portfolios.append(portfolio.model_dump())
    return portfolio


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
