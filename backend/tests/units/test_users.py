import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_and_get_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # ユーザー作成
        create_resp = await ac.post("/users/", json={"id": "user123", "name": "テストユーザー", "email": "test@example.com"})
        assert create_resp.status_code == 200
        assert create_resp.json()["message"] == "User created"

        # ユーザー取得
        get_resp = await ac.get("/users/user123")
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["id"] == "user123"
        assert data["name"] == "テストユーザー"
        assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_list_users():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 事前にユーザーを1件登録しておく
        await ac.post("/users/", json={"id": "user456", "name": "一覧ユーザー", "email": "list@example.com"})

        # 一覧取得
        list_resp = await ac.get("/users/")
        assert list_resp.status_code == 200

        users = list_resp.json().get("users", [])
        assert any(user["id"] == "user456" for user in users)

        print("\n📋 現在のユーザー一覧:")
        for user in users:
            print(user)
