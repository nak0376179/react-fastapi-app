import logging

from botocore.exceptions import ClientError
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel

from app.db.dynamodb import get_table
from app.utils.get_current_user import get_current_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()


# ユーザーモデル定義
class User(BaseModel):
    id: str
    name: str
    email: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


@router.get("/users", tags=["users"])
async def list_users(user: dict = Depends(get_current_user)):
    logger.info(f"valid user: {user.get('cognito:username')}")
    try:
        users_table = get_table("users")
        if users_table:
            response = get_table("users").scan()
            return {"users": response.get("Items", [])}
        else:
            dummy_users = [{"id": "user1", "name": "山田太郎", "email": "taro@example.com"}, {"id": "user2", "name": "鈴木花子", "email": "hanako@example.com"}]
            return {"users": dummy_users}

    except Exception as e:
        print("🔥 list_users 例外:", e)
        # raise HTTPException(status_code=500, detail="Failed to scan users")
        dummy_users = [{"id": "user1", "name": "山田太郎", "email": "taro@example.com"}, {"id": "user2", "name": "鈴木花子", "email": "hanako@example.com"}]
        return {"users": dummy_users}


@router.patch("/users/{user_id}", tags=["users"])
async def update_user_partial(user_id: str, user: UserUpdate = Body(...)):
    update_expr = []
    expr_attrs = {}
    expr_names = {}

    if user.name is not None:
        update_expr.append("#name = :name")
        expr_attrs[":name"] = user.name
        expr_names["#name"] = "name"
    if user.email is not None:
        update_expr.append("email = :email")
        expr_attrs[":email"] = user.email

    if not update_expr:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    try:
        users_table = get_table("users")
        if users_table:
            users_table.update_item(
                Key={"id": user_id},
                UpdateExpression="SET " + ", ".join(update_expr),
                ExpressionAttributeValues=expr_attrs,
                ExpressionAttributeNames=expr_names if expr_names else None,
                ConditionExpression="attribute_exists(id)",
            )
            return {"message": "User updated partially"}
        else:
            raise HTTPException(status_code=404, detail="Users Table not found")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail="User not found")
        print("🔥 update_user_partial 例外:", e)
        raise HTTPException(status_code=500, detail="Failed to update user")


@router.post("/users/", tags=["users"])
async def create_user(user: User):
    try:
        users_table = get_table("users")
        if users_table:
            users_table.put_item(Item=user.model_dump())
            return {"message": "User created", "user": user}
        else:
            raise HTTPException(status_code=404, detail="Users Table not found")

    except ClientError as e:
        print("🔥 create_user 例外:", e)
        raise HTTPException(status_code=500, detail="Failed to create user")


@router.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: str, user: User):
    try:
        users_table = get_table("users")
        if users_table:
            # IDが既に存在している場合のみ更新する
            users_table.put_item(
                Item=user.model_dump(),
                ConditionExpression="attribute_exists(id)",
            )
            return {"message": "User updated", "user": user}
        else:
            raise HTTPException(status_code=404, detail="Users Table not found")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=500, detail="Failed to update user")


@router.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: str):
    try:
        users_table = get_table("users")
        if users_table:
            users_table.delete_item(Key={"id": user_id})
            return {"message": "User deleted"}
        else:
            raise HTTPException(status_code=404, detail="Users Table not found")
    except ClientError as e:
        print("🔥 delete_user 例外:", e)
        raise HTTPException(status_code=500, detail="Failed to delete user")
