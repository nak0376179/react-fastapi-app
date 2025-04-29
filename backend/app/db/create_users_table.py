import boto3
from botocore.exceptions import ClientError

# テーブル名を一元管理
USER_TABLE_NAME = "users"

# DynamoDB リソース（ローカル接続）
dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-northeast-1",
    endpoint_url="http://host.docker.internal:8001",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)


def create_table():
    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
    if USER_TABLE_NAME in existing_tables:
        print(f"✅ テーブル '{USER_TABLE_NAME}' は既に存在します。")
        return

    table = dynamodb.create_table(
        TableName=USER_TABLE_NAME,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    table.wait_until_exists()
    print(f"✅ テーブル '{USER_TABLE_NAME}' を作成しました。")


def insert_items():
    print("👤 ダミーユーザーを追加中...")
    table = dynamodb.Table(USER_TABLE_NAME)
    dummy_users = [
        {"id": "user1", "name": "山田太郎", "email": "taro@example.com"},
        {"id": "user2", "name": "鈴木花子", "email": "hanako@example.com"},
    ]
    for user in dummy_users:
        try:
            table.put_item(Item=user)
            print(f"✅ ユーザー追加: {user['name']}")
        except ClientError as e:
            print(f"❌ 追加失敗: {user['name']}, {e.response['Error']['Message']}")


def show_items():
    table = dynamodb.Table(USER_TABLE_NAME)
    response = table.scan()
    items = response.get("Items", [])
    print("📄 登録ユーザー一覧:")
    for item in items:
        print(item)


if __name__ == "__main__":
    create_table()
    insert_items()
    show_items()
