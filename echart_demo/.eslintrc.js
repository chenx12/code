module.exports = {
  "root": true,
  "env": {
    "node": true
  },
  "extends": [
    "plugin:vue/essential",
    "@vue/typescript"
  ],
  "rules": {
    "semi": [ "warn", "never"],
    "quotes": ["error", "single"],
    // 'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    "space-before-function-paren": [2, {"anonymous": "never", "named": "never"}]
  },
  "parserOptions": {
    "parser": "@typescript-eslint/parser"
  }
}