# General Purpose Agents

General-purpose agents are suitable across many repositories and technology stacks.

## When to Use

- Initial repository onboarding
- Broad code quality and architecture assessments
- Exploratory tasks with unclear requirements
- Template-driven project setup

## Guidelines

- Keep instructions stack-flexible
- Prefer recommendation outputs over auto-mutation
- Document assumptions and confidence levels
- Include clear limits and fallback behavior

## Featured General Agents

- `core/vilabs-configurator` — unified onboarding orchestrator that configures both agent stacks and IDE settings
- `core/vilabs-recruiter` — primary onboarding orchestrator that recruits and configures agent stacks into `.github/`
- `core/vilabs-setting` — IDE settings orchestrator that maps public settings templates to repository-specific configuration plans
- `core/repository-introspector` — analysis-first repository scanner for manual onboarding

See `../docs/creating-agents.md` for creation standards.
