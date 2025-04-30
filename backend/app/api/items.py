import boto3
from fastapi import APIRouter
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
table = dynamodb.Table("items")


# ユーザーモデル定義
class User(BaseModel):
    id: str
    name: str
    email: str


@router.get("/items", tags=["items"])
def get_items():
    response = table.scan()
    return response["Items"]
