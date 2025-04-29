```
% tree -I 'node_modules|.venv|__pycache__'

.
├── README.md
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
│   │   ├── App.css
│   │   ├── App.tsx
│   │   ├── assets
│   │   │   └── react.svg
│   │   ├── index.css
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
├── memo
│   └── memo.md
├── react-fastapi-app.code-workspace
└── scripts
    ├── README.md
    ├── dev.sh
    ├── logs.sh
    ├── reset.sh
    └── stop.sh
```
