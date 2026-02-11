# Example: Node.js GitHub Action

This example demonstrates generating a CI pipeline for a Node.js project using GitHub Actions.

## Input Context

**Project Structure**:

```text
my-web-app/
├── src/
├── package.json
└── package-lock.json
```

**`package.json` scripts**:

```json
"scripts": {
  "build": "next build",
  "test": "jest",
  "lint": "eslint ."
}
```

**User Request**: "Create a GitHub Action to run tests and linting on every PR."

## Agent Action

The agent identifies `package-lock.json` (implying `npm ci` should be used) and specific scripts for testing and linting.

## Output: `.github/workflows/ci.yml`

```yaml
name: Node.js CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test

      - name: Build
        run: npm run build
```

## Effectiveness Note

The agent correctly mapped the user's intent ("tests and linting on PR") to standard GitHub Actions syntax, included matrix testing for multiple Node versions, and utilized caching for performance.
