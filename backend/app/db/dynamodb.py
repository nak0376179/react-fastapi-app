# app/db/dynamodb.py
import os

import boto3

from . import create_items_table, create_users_table


def get_table(table_name: str):
    """DynamoDBのテーブルを取得します。ローカル環境ではDynamoDB Localから取得します。"""
    env = os.environ.get("ENVIRONMENT", "local")
    use_dynamodb_local = env == "local"

    if use_dynamodb_local:
        dynamodb = boto3.resource(
            "dynamodb",
            region_name="ap-northeast-1",
            endpoint_url="http://host.docker.internal:8001",
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
        )
        return dynamodb.Table(table_name)
    else:
        # 本番環境など、設定されたAWSの資格情報で実行される
        dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
        return dynamodb.Table(table_name)


def init_tables():
    """DynamoDB Localを初期設定します。ローカル環境のみ実行可能です。"""
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="ap-northeast-1",
        endpoint_url="http://host.docker.internal:8001",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )

    existing = dynamodb.meta.client.list_tables()["TableNames"]

    for table_name in ["users", "items"]:
        if table_name not in existing:
            print(f"⚠️ Table '{table_name}' を作成します。")
            create_users_table.create_table()
            create_users_table.insert_items()
            create_items_table.create_table()
            create_items_table.insert_items()
        else:
            print(f"✅ Table '{table_name}' は作成済みです。")
