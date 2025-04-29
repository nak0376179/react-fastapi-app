FROM python:3.12-slim

WORKDIR /app

# pip-tools（ロック生成ツール）インストール
RUN pip install --no-cache-dir pip-tools

# requirements.inとrequirements.txtを先にCOPY
COPY requirements.in requirements.txt ./

# requirements.txtからインストール（ロックファイルに従う）
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体をコピー
COPY . .

# FastAPI（Uvicorn）起動コマンド
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
