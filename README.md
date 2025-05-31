# Cross Border Trade Lens

Cross Border Trade Lens is a simple Next.js 14 boilerplate set up with TypeScript, Tailwind CSS and a few useful developer tools like ESLint, Prettier and Husky.

## Prerequisites

- **Node.js** v20 or newer
- **pnpm**

## Setup

1. `cd frontend`
2. Run `pnpm install` to install dependencies. The `prepare` script will automatically run `husky install` so Git hooks are ready.
3. Start the development server with `pnpm dev`.

## Scripts

- `pnpm lint` – run ESLint
- `pnpm format` – format with Prettier
- `pnpm run check` – run the linter (used for CI or pre-commit)

Husky's pre-commit hook runs `pnpm lint` and `pnpm format` before each commit.
