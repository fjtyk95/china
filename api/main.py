from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routes import billing, jobs
from .routers import router  # 既存の共通ルーター

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 簡易ヘルスチェック
@app.get("/ping")
async def ping():
    return {"msg": "pong"}

# ルーターの登録
app.include_router(router)
app.include_router(billing.router)
app.include_router(jobs.router, prefix="/v1")
