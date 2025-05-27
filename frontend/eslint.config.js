const { FlatCompat } = require('@eslint/eslintrc');
const eslintrc = require('./.eslintrc.json');

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

module.exports = compat.config(eslintrc);
