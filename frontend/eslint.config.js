const { FlatCompat } = require('@eslint/eslintrc');

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

module.exports = compat.config({
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
