from fastapi import FastAPI
from api.height import height_router

from starlette.middleware.cors import CORSMiddleware

# fastapi記事以下参照
# https://www.sukerou.com/2021/06/anacondafastapi.html

# インストール
# conda install -c conda-forge fastapi uvicorn
# サーバー立てるコマンド
# uvicorn run_api:app --reload

app = FastAPI()

# CORS回避のための記述
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーティングの設定
app.include_router(height_router, prefix="/height")


@app.get("/")
async def root():
    return {"message": "Hello World"}