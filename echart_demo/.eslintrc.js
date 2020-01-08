module.exports = {
  "root": true,
  "env": {
    "node": true
  },
  "extends": [
    "plugin:vue/essential",
    "@vue/prettier",
    "@vue/typescript"
  ],
  "rules": {
    "semi": [ "error", "never"],
    "quotes": ["error", "single"]
  },
  "parserOptions": {
    "parser": "@typescript-eslint/parser"
  }
}