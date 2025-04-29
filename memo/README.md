# docker で開発環境を作りたい

## 概要

frontend と backend を docker-compose で管理したい。

## FrontEnd

- Vite+React+SWC で 5173 ポートを使う
- node_modules はコンテナの外に置いて、ホットリロードを効かせたいです。

## Backend

- FastAPI で 8000 ポートを使う
- .venv を ./backend に設置して使いたい。
- こちらも app はコンテナの外に置いて、ホットリロードを効かせたいです。

## その他

- devcontainer は使えないかもしれませんが利用できるようにセットアップしたいです。
- リポジトリは aws codecommit または github を利用します。

以下の設定ファイルを考えました。

.vscode/extention.json

```
{
  "recommendations": [
    "editorconfig.editorconfig",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-vscode.live-server",
    "shd101wyy.markdown-preview-enhanced",
    "vitest.explorer",
    "ms-python.python",
    "charliermarsh.ruff"
  ]
}
```

.vscode/settings.json

```
 {
  // Pythonはruffを使う
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  // React系 (JS/TS/HTML/CSS/JSON/Markdown) はPrettierを使う
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[html]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[css]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[markdown]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },

  // 共通設定
  "python.autoComplete.extraPaths": ["./backend"],
  "python.defaultInterpreterPath": "./backend/.venv/bin/python",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit",
    "source.organizeImports": "explicit"
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```
