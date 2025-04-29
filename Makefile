.PHONY: help up stop down ps status logs test backend-test frontend-test backend-shell frontend-shell build clean

up:  ## サービスを起動（再ビルドせず）
	@echo "🔼 コンテナを起動中..."
	docker-compose up -d

stop:  ## コンテナを停止
	@echo "⏹️ コンテナを停止中..."
	docker-compose stop

down:  ## コンテナとボリュームを含めて完全停止・削除
	@echo "🧹 コンテナとボリュームを完全削除中..."
	docker-compose down -v

status:  ## サービスのステータス＋ログの先頭を表示
	@echo "📊 サービスのステータス:"
	docker-compose ps
	@echo "\n--- Backend Logs (last 5 lines) ---"
	docker-compose logs backend --tail=5
	@echo "\n--- Frontend Logs (last 5 lines) ---"
	docker-compose logs frontend --tail=5

logs:  ## ログをリアルタイムで表示
	docker-compose logs -f --tail=100

backend-shell:  ## backend コンテナにシェルで入る
	@echo "🖥️ backend にログイン中..."
	docker-compose exec backend /bin/sh

frontend-shell:  ## frontend コンテナにシェルで入る
	@echo "🖥️ frontend にログイン中..."
	docker-compose exec frontend /bin/sh

build:  ## イメージをビルド
	@echo "🔧 イメージをビルド中..."
	docker-compose build

clean:  ## 軽めのクリーン（dangling images は残す）
	@echo "🧼 未使用リソースを削除中..."
	docker system prune -f

clean-all:  ## 完全なクリーン（未使用イメージ含む）
	@echo "🧼 未使用リソースを削除中..."
	docker system prune -a -f
	@echo "🗑️ 未タグのイメージを削除中..."
	docker image prune -f

# テスト系
test: backend-test  ## 全体のテスト（現状は backend のみ）

backend-test:  ## backend（FastAPI）のテストを実行
	docker-compose exec backend pytest

verbose-backend-test:  ## backend のテストを出力付きで実行
	docker-compose exec backend pytest -s

frontend-test:  ## frontend（Vite + Vitest）のテストを実行
	docker-compose exec frontend npm run test

# DynamoDB操作系
create-tables: ## DynamoDB テーブル（例：users）を作成
	docker-compose exec backend python app/db/create_users_table.py
	docker-compose exec backend python app/db/create_items_table.py

delete-tables: ## DynamoDBローカルの全テーブルを削除して再作成する
	docker-compose exec backend python scripts/delete_all_tables.py

# 状態確認
ps:  ## 現在起動中のサービス一覧を表示
	docker-compose ps

help:  ## 使用可能な make コマンド一覧を表示
	@echo "使用可能な make コマンド一覧："
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

