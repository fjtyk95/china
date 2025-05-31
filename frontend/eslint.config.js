module.exports = [
  {
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
  },
];
