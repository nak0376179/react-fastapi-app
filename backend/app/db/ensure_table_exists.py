# db.py
import boto3

from . import create_items_table, create_users_table

dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-northeast-1",
    endpoint_url="http://host.docker.internal:8001",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)


def ensure_table_exists(table_name: str):
    existing = dynamodb.meta.client.list_tables()["TableNames"]
    if table_name not in existing:
        print(f"⚠️ Table '{table_name}' not found.")
        create_users_table.create_table()
        create_users_table.insert_items()
        create_items_table.create_table()
        create_items_table.insert_items()

    else:
        print(f"✅ Table '{table_name}' exists.")
