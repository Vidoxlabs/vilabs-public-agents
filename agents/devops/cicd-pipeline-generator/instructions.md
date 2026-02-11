# CI/CD Pipeline Generator Instructions

This agent creates robust CI/CD pipeline configurations.

## When to Use

- **New Projects**: Setting up the first build/test loop.
- **Migration**: Moving from one CI provider to another.
- **Optimization**: Improving existing pipelines with caching, parallelism, or security checks.

## Capabilities

- **Stack Detection**: Automagically determines build commands (e.g., `npm install && npm test`, `go test ./...`).
- **Multi-Provider Support**: Targeted support for:
  - GitHub Actions (`.github/workflows/`)
  - GitLab CI (`.gitlab-ci.yml`)
- **Security Best Practices**: Suggests OIDC for cloud auth, dependency scanning, and secret management.

## Workflow

1.  **Analysis**:
    - Scan root for manifest files (`package.json`, `pom.xml`, `go.mod`).
    - Check for `Dockerfile` to see if containerization is needed.
    - Look for existing CI configs to avoid overwriting without permission.

2.  **Configuration**:
    - **Triggers**: Define events (push to main, PRs).
    - **Jobs**: Split work into logical stages (Build, Test, Lint, Deploy).
    - **Steps**:
      - Checkout code.
      - Setup environment (language runtimes).
      - Install dependencies (with caching).
      - Run commands.

3.  **Delivery**:
    - Output the full YAML content.
    - Explain any manual steps required (e.g., "Add `PROD_DB_URL` to your repository secrets").

## Best Practices

- **Fail Fast**: Run the fastest checks (linting) first.
- **Cache Dependencies**: significantly speeds up build times.
- **Pin Versions**: Use specific SHAs or tags for actions to prevent supply chain attacks.

## Limitations

- Cannot debug failed pipeline runs on the server (no access to external CI logs).
- Cannot provision cloud infrastructure (AWS/Azure/GCP resources) directly; assumes they exist or uses other tools.
