# cross-border-trade-lens

このリポジトリは Next.js 14 を使用したフロントエンドのボイラープレートです。

## 前提条件
- Node.js 18 以上
- pnpm 8 以上

## セットアップ
```bash
cd frontend
pnpm install
```

## 開発サーバー起動
```bash
pnpm dev
```

## スクリプト
- `pnpm lint` : ESLint によるコードチェック
- `pnpm format` : Prettier での整形
- `pnpm run check` : lint と型チェックを実行

コミット前に Husky が自動で `pnpm lint` と `pnpm format` を実行します。
