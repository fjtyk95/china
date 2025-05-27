import { FlatCompat } from '@eslint/eslintrc';

const compat = new FlatCompat({ baseDirectory: __dirname });
export default compat.config({
  ignores: ['node_modules', '.next'],
  extends: [
    'airbnb',
    'airbnb/hooks',
    'airbnb-typescript',
    'next/core-web-vitals',
  ],
  parserOptions: {
    project: './tsconfig.json',
  },
  rules: {},
});
