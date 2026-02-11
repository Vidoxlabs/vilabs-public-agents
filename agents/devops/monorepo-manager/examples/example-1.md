# Example: Refactoring a Monorepo for Scalability

## Input

A monorepo experiencing circular dependencies and architectural issues as the team scales.

**Current Structure Issues**:

```
monorepo/
├── apps/
│   ├── web/
│   │   └── src/
│   │       ├── components/Button.tsx      # Also in packages/ui
│   │       ├── api/useAuth.ts            # Auth logic duplicated
│   │       └── types/Auth.ts              # Also in packages/types
│   ├── dashboard/
│   │   └── src/
│   │       ├── components/Button.tsx      # Duplicate of web
│   │       └── utils/formatters.ts        # Duplicated code
│   └── api/
│       └── src/
│           ├── routes/auth.ts             # Imports from apps/web
│           └── schemas/index.ts           # Also in packages/schemas
├── packages/
│   ├── ui/
│   │   └── Button.tsx                    # Different Button than apps/
│   ├── types/
│   │   └── Auth.ts
│   └── schemas/
│       └── index.ts
└── turbo.json
```

**Problems Identified**:

- Button component duplicated in 3 places
- Auth types defined in multiple packages
- API imports from frontend app (boundary violation)
- No explicit exports defined
- TurboRepo not optimized for caching

## Output

### 📦 Monorepo Structure Review

**Project**: Multi-app Platform
**Build System**: TurboRepo
**Language**: TypeScript
**Package Manager**: pnpm

#### Dependency Graph Issues

**Current State** (Problematic):

```
apps/web ──→ packages/types
apps/web ──→ packages/schemas
apps/dashboard ──→ packages/ui
apps/api ──→ apps/web  ❌ CIRCULAR
apps/api ──→ packages/schemas
```

#### Issues Identified

**Critical** 🔴

1. **Boundary Violation: API Imports Frontend**
   - **Location**: `apps/api/src/routes/auth.ts` imports from `apps/web`
   - **Impact**: Creates circular dependency; violates architecture
   - **Fix**: Extract shared logic to `packages/auth`

2. **Circular Dependencies Detected**
   - **Cycle**: apps/web → packages/types → apps/api → apps/web
   - **Impact**: Build system confusion; test execution issues
   - **Fix**: Move shared types to independent `packages/types`

3. **Massive Code Duplication**
   - **Button Component**: Duplicated 3 times
   - **Auth Logic**: Duplicated in apps/web and apps/api
   - **Formatters**: Duplicated in apps/dashboard and apps/web
   - **Impact**: Maintenance nightmare; inconsistency
   - **Fix**: Centralize in packages/

**High** 🟠

4. **Missing Package Exports**
   - **Issue**: Packages have no `exports` field in `package.json`
   - **Impact**: Consumers can import internal paths
   - **Fix**: Define strict `exports` for each package

5. **TurboRepo Not Optimized**
   - **Issue**: No task dependencies configured
   - **Impact**: Rebuilds unnecessary packages
   - **Fix**: Configure caching and task dependencies

#### Recommended Structure

```
monorepo/
├── apps/
│   ├── web/
│   │   ├── src/
│   │   │   ├── pages/        # Web-specific pages only
│   │   │   ├── hooks/        # Web-specific hooks
│   │   │   └── layouts/      # Web layouts
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── dashboard/
│   │   └── (similar structure)
│   └── api/
│       ├── src/
│       │   ├── routes/       # API routes
│       │   ├── middleware/   # API middleware
│       │   └── services/     # Business logic
│       ├── package.json
│       └── tsconfig.json
├── packages/
│   ├── ui/                   # ✓ Shared UI components
│   │   ├── src/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   └── index.ts
│   │   ├── package.json      # With exports
│   │   └── tsconfig.json
│   ├── types/                # ✓ Centralized types
│   │   ├── src/
│   │   │   ├── auth.ts
│   │   │   ├── api.ts
│   │   │   └── index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── auth/                 # ✓ Extracted logic
│   │   ├── src/
│   │   │   ├── hooks/
│   │   │   │   └── useAuth.ts
│   │   │   ├── utils/
│   │   │   │   └── tokenManager.ts
│   │   │   └── index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── utils/                # ✓ Common utilities
│   │   ├── src/
│   │   │   ├── formatters.ts
│   │   │   ├── validators.ts
│   │   │   └── index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── schemas/              # ✓ Validation schemas
│       ├── src/
│       │   ├── auth.ts
│       │   ├── api.ts
│       │   └── index.ts
│       ├── package.json
│       └── tsconfig.json
├── turbo.json                # ✓ Optimized
├── pnpm-workspace.yaml
└── tsconfig.json             # Base config
```

#### Dependency Graph (Corrected)

```
✓ Correct Flow (No Cycles):
apps/web ────→ packages/ui
apps/web ────→ packages/types
apps/web ────→ packages/auth
apps/web ────→ packages/schemas
apps/web ────→ packages/utils

apps/dashboard ────→ packages/ui
apps/dashboard ────→ packages/types
apps/dashboard ────→ packages/utils

apps/api ────→ packages/types
apps/api ────→ packages/schemas
apps/api ────→ packages/utils
```

**Key**: No app imports from another app. No cycles.

#### Configuration Changes

**`packages/ui/package.json`** (New)

```json
{
  "name": "@myapp/ui",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    ".": "./dist/index.js",
    "./Button": "./dist/Button.js",
    "./Card": "./dist/Card.js",
    "./*": "./dist/*"
  },
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
```

**`packages/auth/package.json`** (New)

```json
{
  "name": "@myapp/auth",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    ".": "./dist/index.js",
    "./hooks": "./dist/hooks/index.js",
    "./utils": "./dist/utils/index.js"
  },
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "dependencies": {
    "@myapp/types": "workspace:*"
  }
}
```

**Root `pnpm-workspace.yaml`**

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

**Root `tsconfig.json`** (Paths)

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@myapp/ui": ["packages/ui/src/index.ts"],
      "@myapp/ui/*": ["packages/ui/src/*"],
      "@myapp/types": ["packages/types/src/index.ts"],
      "@myapp/types/*": ["packages/types/src/*"],
      "@myapp/auth": ["packages/auth/src/index.ts"],
      "@myapp/auth/*": ["packages/auth/src/*"],
      "@myapp/utils": ["packages/utils/src/index.ts"],
      "@myapp/utils/*": ["packages/utils/src/*"],
      "@myapp/schemas": ["packages/schemas/src/index.ts"],
      "@myapp/schemas/*": ["packages/schemas/src/*"]
    }
  }
}
```

**`turbo.json`** (Build Optimization)

```json
{
  "$schema": "https://turborepo.org/schema.json",
  "globalDependencies": ["**/.env.local", ".env"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"],
      "cache": true
    },
    "lint": {
      "outputs": [],
      "cache": false
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"],
      "cache": true
    },
    "type-check": {
      "dependsOn": ["^build"],
      "cache": true,
      "outputs": []
    }
  }
}
```

#### Migration Steps

1. **Create New Packages**

   ```bash
   mkdir -p packages/{ui,auth,utils,schemas,types}
   # Copy relevant files, configure package.json
   ```

2. **Extract Components**
   - Move Button from `apps/web` to `packages/ui`
   - Move auth hooks to `packages/auth/hooks`
   - Move formatters to `packages/utils`

3. **Update Imports**

   ```typescript
   // Before
   import Button from "../../../components/Button";

   // After
   import { Button } from "@myapp/ui";
   ```

4. **Fix API Imports**

   ```typescript
   // Before - WRONG (boundary violation)
   import { useAuth } from "../../apps/web/hooks";

   // After - CORRECT
   import { useAuth } from "@myapp/auth/hooks";
   ```

5. **Add Exports**
   - Define `exports` field in each package.json
   - Update `tsconfig.json` paths

6. **Update Build Config**
   - Configure `turbo.json` task dependencies
   - Test build caching

7. **Update CI/CD**
   - Configure to only rebuild affected packages
   - Test with monorepo changes

## Context

This example demonstrates:

- Identifying duplicate code across monorepo
- Detecting circular dependencies
- Enforcing architectural boundaries
- Proposing clear package organization
- Providing migration steps
- Build system optimization

## Effectiveness

- **Issues Fixed**: ✓ Circular dependencies eliminated
- **Code Quality**: ✓ Duplication removed
- **Architecture**: ✓ Clear boundaries established
- **Build Performance**: ✓ Caching enabled
- **Developer Experience**: ✓ Clear import paths

**Notes**: This restructuring transforms a monorepo from chaotic to scalable, enabling the team to grow without architectural degradation. Regular code reviews using package boundary rules are essential for maintenance.
