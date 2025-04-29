.PHONY: help up stop down ps status logs test backend-test frontend-test backend-shell frontend-shell build clean

help:  ## 使用可能な make コマンド一覧を表示
	@echo "使用可能な make コマンド一覧："
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

up:  ## サービスを起動（再ビルドせず）
	@echo "🔼 コンテナを起動中..."
	docker-compose up -d

stop:  ## コンテナを停止
	@echo "⏹️ コンテナを停止中..."
	docker-compose stop

down:  ## コンテナとボリュームを含めて完全停止・削除
	@echo "🧹 コンテナとボリュームを完全削除中..."
	docker-compose down -v

ps:  ## 現在起動中のサービス一覧を表示
	docker-compose ps

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

clean:  ## 未使用のリソースを削除（docker system prune）
	@echo "🧼 未使用リソースを削除中..."
	docker system prune -f

test: backend-test  ## 全体のテスト（現状は backend のみ）

backend-test:  ## backend（FastAPI）のテストを実行
	docker-compose exec backend pytest

frontend-test:  ## frontend（Vite + Vitest）のテストを実行
	docker-compose exec frontend npm run test
