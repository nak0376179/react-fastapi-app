以下の構成を組みました。

docker-compose.yml

```
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5173:5173"     # Viteデフォルトポートをホストに公開
    volumes:
      - ./frontend:/app  # ローカルのfrontendソースコードをコンテナの/appにマウント（ホットリロード対応）
      - /app/node_modules # node_modulesはコンテナ内で専用管理（ローカルとは分離）
    environment:
      - NODE_ENV=development # Node.jsを開発モードに設定
      - CHOKIDAR_USEPOLLING=true  # Docker内でファイル監視を強制的に有効化（ホットリロードのため）
    command: sh -c "npm ci || npm install && npm run dev -- --host"
    platform: linux/amd64 # amd64アーキテクチャを指定（Apple Silicon対策など）
    depends_on:
      - backend
    networks:
      - app-network

  backend:
    build: ./backend  # バックエンド（FastAPI）用のDockerfile
    ports:
      - "8000:8000"     # FastAPIサーバーポート
    volumes:
      - ./backend:/app  # ソースコードをマウントして即時反映
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] # FastAPI起動コマンド
    platform: linux/amd64
    environment:
      - PYTHONUNBUFFERED=1  # ログ即出力設定（バッファリング無効化）
    networks:
      - app-network

networks:
  app-network:
    driver: bridge  # 全サービス共通ネットワーク
```

% tree -I 'node_modules|.venv|**pycache**'

```
.
├── backend
│   ├── Dockerfile
│   ├── app
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── root.py
│   │   │   └── users.py
│   │   └── main.py
│   ├── pyproject.toml
│   ├── requirements.in
│   └── requirements.txt
├── docker-compose.yml
├── frontend
│   ├── Dockerfile
│   ├── README.md
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── prettier.config.cjs
│   ├── public
│   │   └── vite.svg
│   ├── src
│   │   ├── App.test.tsx
│   │   ├── App.tsx
│   │   ├── assets
│   │   ├── index.css
│   │   ├── main.tsx
│   │   ├── stories
│   │   │   ├── Button.stories.ts
│   │   │   ├── Button.tsx
│   │   │   ├── Configure.mdx
│   │   │   ├── Header.stories.ts
│   │   │   ├── Header.tsx
│   │   │   ├── Page.stories.ts
│   │   │   ├── Page.tsx
│   │   │   ├── assets
│   │   │   │   ├── accessibility.png
│   │   │   │   ├── accessibility.svg
│   │   │   │   ├── addon-library.png
│   │   │   │   ├── assets.png
│   │   │   │   ├── avif-test-image.avif
│   │   │   │   ├── context.png
│   │   │   │   ├── discord.svg
│   │   │   │   ├── docs.png
│   │   │   │   ├── figma-plugin.png
│   │   │   │   ├── github.svg
│   │   │   │   ├── share.png
│   │   │   │   ├── styling.png
│   │   │   │   ├── testing.png
│   │   │   │   ├── theming.png
│   │   │   │   ├── tutorials.svg
│   │   │   │   └── youtube.svg
│   │   │   ├── button.css
│   │   │   ├── header.css
│   │   │   └── page.css
│   │   ├── themes.ts
│   │   └── vite-env.d.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   ├── vitest.config.ts
│   ├── vitest.shims.d.ts
│   └── vitest.workspace.ts
├── memo
│   ├── README.md
│   ├── chatgpt.md
│   ├── git.md
│   ├── memo.md
│   ├── mui.md
│   ├── storybook.md
│   └── vitest.md
├── package-lock.json
├── package.json
├── react-fastapi-app.code-workspace
└── scripts
    ├── README.md
    ├── dev.sh
    ├── logs.sh
    ├── reset.sh
    └── stop.sh
```
