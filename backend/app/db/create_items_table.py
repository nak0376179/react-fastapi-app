import boto3
from botocore.exceptions import ClientError

# テーブル名を一元管理
TABLE_NAME = "items"

# DynamoDB リソース（ローカル接続）
dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-northeast-1",
    endpoint_url="http://host.docker.internal:8001",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)


def create_table():
    table_name = TABLE_NAME

    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
    if table_name in existing_tables:
        print(f"✅ テーブル '{table_name}' は既に存在します。")
        return

    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}, {"AttributeName": "title", "KeyType": "RANGE"}],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "N"},
                {"AttributeName": "title", "AttributeType": "S"},
                {"AttributeName": "price", "AttributeType": "N"},
                {"AttributeName": "category", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "category-price-index",
                    "KeySchema": [{"AttributeName": "category", "KeyType": "HASH"}, {"AttributeName": "price", "KeyType": "RANGE"}],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
                },
                {
                    "IndexName": "category-title-index",
                    "KeySchema": [{"AttributeName": "category", "KeyType": "HASH"}, {"AttributeName": "title", "KeyType": "RANGE"}],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
                },
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.wait_until_exists()
        print(f"Created table {table_name}")
    except ClientError as e:
        print(f"Failed to create {table_name}: {e.response['Error']['Message']}")


def insert_items():
    table = dynamodb.Table(TABLE_NAME)
    items = [
        {"id": 101, "title": "Book A", "price": 10, "category": "book"},
        {"id": 102, "title": "Book B", "price": 15, "category": "book"},
        {"id": 201, "title": "Bike A", "price": 100, "category": "bike"},
    ]
    for item in items:
        table.put_item(Item=item)
    print("Loaded sample data")


if __name__ == "__main__":
    create_table()
    insert_items()
