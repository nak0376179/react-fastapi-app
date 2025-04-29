FROM node:22

# 作業ディレクトリを/appに設定
WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
# （ここでコピーすると、依存だけ変わった時にキャッシュが効く）
COPY package.json package-lock.json ./

# 依存パッケージをインストール
RUN npm install

# それ以外のアプリケーションソースコードをコピー
COPY . .

# Vite開発サーバーを起動（--hostオプションで外部アクセス許可）
CMD ["npm", "run", "dev", "--", "--host"]
