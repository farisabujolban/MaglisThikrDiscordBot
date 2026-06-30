/** @type {import('lint-staged').Configuration} */
const config = {
    '*.py': ['ruff check --fix', 'ruff format'],
};

export default config;
