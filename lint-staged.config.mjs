/** @type {import('lint-staged').Configuration} */
const config = {
    '*': 'prettier --ignore-unknown --write',
    '*.{ts,tsx,js,jsx,mjs,cjs}': 'eslint --no-warn-ignored --max-warnings=0 --fix --cache',
};

export default config;
