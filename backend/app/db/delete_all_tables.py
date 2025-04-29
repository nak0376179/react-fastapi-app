# scripts/reset_all_tables.py
import time

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://host.docker.internal:8001",
    region_name="us-west-2",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)


def delete_all_tables():
    client = dynamodb.meta.client
    table_names = client.list_tables()["TableNames"]
    if not table_names:
        print("ℹ️ No tables to delete.")
        return

    for table_name in table_names:
        print(f"💥 Deleting table: {table_name}")
        table = dynamodb.Table(table_name)
        try:
            table.delete()
            table.wait_until_not_exists()
        except ClientError as e:
            print(f"⚠️ Failed to delete {table_name}: {e}")
        time.sleep(0.5)


if __name__ == "__main__":
    delete_all_tables()
