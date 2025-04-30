import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import items, root, users
from app.db.dynamodb import init_tables
from app.utils.access_logger import AccessLoggerMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)

# 環境変数 ENVIRONMENT が 'local' のときだけ lifespan を使ってDynamoDBを初期化する
env = os.environ.get("ENVIRONMENT", "local")
use_lifespan = env == "local"


async def lifespan(app: FastAPI):
    print("startup event")
    init_tables()
    yield
    print("shutdown event")


app = FastAPI(
    title="FastAPIアプリケーション",
    version="1.0.0",
    openapi_tags=[
        {"name": "root", "description": "health"},
        {"name": "users", "description": "Users管理に関する操作。"},
        {"name": "items", "description": "Items管理に関する操作。"},
    ],
    lifespan=lifespan if use_lifespan else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AccessLoggerMiddleware)


# ルートをモジュールからインクルード
app.include_router(root.router)
app.include_router(users.router)
app.include_router(items.router)
