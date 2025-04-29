import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

router = APIRouter()

# DynamoDB 接続設定
dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-northeast-1",
    endpoint_url="http://host.docker.internal:8001",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)
user_table = dynamodb.Table("users")


# ユーザーモデル定義
class User(BaseModel):
    id: str
    name: str
    email: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


@router.get("/users/", tags=["users"])
async def list_users():
    try:
        response = user_table.scan()
        return {"users": response.get("Items", [])}
    except Exception as e:
        print("🔥 list_users 例外:", e)
        raise HTTPException(status_code=500, detail="Failed to scan users")


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
        user_table.update_item(
            Key={"id": user_id},
            UpdateExpression="SET " + ", ".join(update_expr),
            ExpressionAttributeValues=expr_attrs,
            ExpressionAttributeNames=expr_names if expr_names else None,
            ConditionExpression="attribute_exists(id)",
        )
        return {"message": "User updated partially"}
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail="User not found")
        print("🔥 update_user_partial 例外:", e)
        raise HTTPException(status_code=500, detail="Failed to update user")


@router.post("/users/", tags=["users"])
async def create_user(user: User):
    try:
        user_table.put_item(Item=user.model_dump())
        return {"message": "User created", "user": user}
    except ClientError as e:
        print("🔥 create_user 例外:", e)
        raise HTTPException(status_code=500, detail="Failed to create user")


@router.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: str, user: User):
    try:
        # IDが既に存在している場合のみ更新する
        user_table.put_item(
            Item=user.model_dump(),
            ConditionExpression="attribute_exists(id)",
        )
        return {"message": "User updated", "user": user}
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=500, detail="Failed to update user")


@router.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: str):
    try:
        user_table.delete_item(Key={"id": user_id})
        return {"message": "User deleted"}
    except ClientError as e:
        print("🔥 delete_user 例外:", e)
        raise HTTPException(status_code=500, detail="Failed to delete user")
