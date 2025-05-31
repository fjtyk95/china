# Cross Border Trade Lens

このリポジトリは Next.js 14 を用いたフロントエンドのボイラープレートです。
TypeScript、Tailwind CSS、ESLint、Prettier、Husky などが事前に設定されています。

## 前提条件 / Prerequisites
- Node.js 18 以上 (推奨 20 以上)
- pnpm 8 以上

## セットアップ / Setup
1. `cd frontend`
2. `pnpm install` を実行すると `husky install` が自動で走ります
3. `pnpm dev` で開発サーバーを起動

## スクリプト / Scripts
- `pnpm lint` – ESLint によるコードチェック
- `pnpm format` – Prettier で整形
- `pnpm run check` – lint を実行 (CI や pre-commit 用)

Husky の pre-commit フックによってコミット前に `pnpm lint` と `pnpm format` が実行されます。
