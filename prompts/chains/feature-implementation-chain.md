# Feature Implementation Chain (Stack-Agnostic)

Use this chain to plan and implement features across unknown repository structures.

## Inputs

- `{{feature_goal}}`: Business/technical outcome
- `{{affected_layers}}`: Data, API, UI, jobs, infra
- `{{repo_layout}}`: Key paths discovered by repository analysis
- `{{constraints}}`: Security, performance, compliance, delivery timeline

## Phase 1: Discovery and Scope

<reasoning>
1. Identify impacted components from repository structure.
2. Define in-scope and out-of-scope changes.
3. Enumerate assumptions and unresolved dependencies.
</reasoning>

## Phase 2: Contract and Data Design

<reasoning>
1. Define data model changes (if needed).
2. Define interface contracts (request/response/events).
3. Specify backward compatibility and migration strategy.
</reasoning>

## Phase 3: Implementation Plan by Layer

<reasoning>
1. Backend/service changes.
2. Frontend/client changes.
3. Shared package or schema updates.
4. Infra/config changes where required.
</reasoning>

## Phase 4: Verification and Rollout

<reasoning>
1. Define test coverage for happy path, edge cases, and failures.
2. Define observability and rollback approach.
3. Define acceptance criteria mapped to `{{feature_goal}}`.
</reasoning>

## Output Format

Return a file-by-file implementation sequence using discovered repository paths, including:

1. File path
2. Change summary
3. Validation command(s)
4. Risks and mitigations
