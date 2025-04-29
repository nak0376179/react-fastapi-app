from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import root, users

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
