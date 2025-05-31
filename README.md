# Cross Border Trade Lens

## プロジェクト概要
Cross Border Trade Lens は Next.js 14 を利用したフロントエンドと、AWS 上のインフラを構築する Terraform 定義をまとめたリポジトリです。
フロントエンドは TypeScript と Tailwind CSS を採用し、開発効率向上のため ESLint、Prettier、Husky などのツールが設定されています。
Terraform では S3 バケットや RDS(PostgreSQL) を作成します。

## 前提条件
- Node.js 18 以上 (推奨 20 以上)
- pnpm 8 以上
- Terraform 1.7 以上
- AWS CLI などで認証情報を設定済みであること

## セットアップ
### フロントエンド
1. `cd frontend`
2. `pnpm install` を実行すると `husky install` が自動で走ります
3. `pnpm dev` で開発サーバーを起動

### インフラストラクチャ
1. `cd terraform`
2. `terraform init` でプロバイダーを初期化
3. `terraform apply` を実行してリソースを作成 (必要に応じて `-var` オプションで値を指定)

## 主要スクリプト
### フロントエンド
- `pnpm dev` – 開発サーバーを起動
- `pnpm build` – 本番ビルドを作成
- `pnpm start` – 本番ビルドを起動
- `pnpm lint` – ESLint によるコードチェック
- `pnpm format` – Prettier で整形
- `pnpm run check` – lint と型チェックを実行 (CI や pre-commit 用)

### インフラストラクチャ
- `terraform init` – Terraform の初期化
- `terraform plan` – 適用前の変更内容を確認
- `terraform apply` – 変更を適用

Husky の pre-commit フックによってコミット前に `pnpm lint` と `pnpm format` が実行されます。
