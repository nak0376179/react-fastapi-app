from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import items, root, users
from .db.ensure_table_exists import ensure_table_exists


async def lifespan(app: FastAPI):
    print("startup event")
    ensure_table_exists("user")
    ensure_table_exists("items")
    yield
    print("shutdown event")


app = FastAPI(
    title="PDFアプリケーション",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "root",
            "description": "health",
        },
        {
            "name": "users",
            "description": "ユーザー管理に関する操作。",
        },
    ],
    # dependencies=[Depends(verify_token)]
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ルートをモジュールからインクルード
app.include_router(root.router)
app.include_router(users.router)
app.include_router(items.router)
