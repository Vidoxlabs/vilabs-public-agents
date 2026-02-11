# Example: Docker Compose & Documentation Validation

## Input

Review a microservice architecture for consistency between documentation and Docker Compose configuration.

**Documentation** (`README.md`):

```markdown
# Microservice Architecture

## Services

### API Service

- Port: 8000
- Image: fastapi:v2.0.0
- Environment: NODE_ENV=production

### Cache Service (Redis)

- Port: 6379
- Image: redis:7.0.0

### Database (PostgreSQL)

- Port: 5432
- Image: postgres:15.0
```

**Implementation** (`docker-compose.yml`):

```yaml
version: "3.8"
services:
  api:
    image: fastapi:v2.0.1
    ports:
      - "8001:8000"
    environment:
      NODE_ENV: staging

  cache:
    image: redis:7.0.0
    ports:
      - "6379:6379"

  database:
    image: postgres:14.0
    ports:
      - "5432:5432"
```

## Output

### 📑 Consistency Check Report

**System**: Microservice Architecture
**Documentation**: README.md (updated 2026-01-15)
**Implementation**: docker-compose.yml (updated 2026-02-01)
**Drift Detected**: ✅ Yes - 3 Critical Discrepancies

#### Synchronization Status

| Component       | Documented     | Actual         | Status   | Severity |
| --------------- | -------------- | -------------- | -------- | -------- |
| API Image       | fastapi:v2.0.0 | fastapi:v2.0.1 | ⚠️ Drift | Medium   |
| API Port        | 8000           | 8001           | ❌ Drift | **High** |
| API Environment | production     | staging        | ❌ Drift | **High** |
| Redis Port      | 6379           | 6379           | ✓ Sync   | —        |
| Redis Image     | redis:7.0.0    | redis:7.0.0    | ✓ Sync   | —        |
| DB Image        | postgres:15.0  | postgres:14.0  | ❌ Drift | Medium   |
| DB Port         | 5432           | 5432           | ✓ Sync   | —        |

#### 🚨 Critical Discrepancies

**High Priority** 🔴

1. **API Port Mismatch**
   - Documented: 8000
   - Actual: 8001
   - Impact: Clients connecting to documented port will fail
   - Root Cause: Local development port mapping differs from prod config

2. **API Environment Mismatch**
   - Documented: production
   - Actual: staging
   - Impact: Wrong configuration loaded; security implications
   - Root Cause: Staging config committed instead of production

**Medium Priority** 🟡

3. **API Image Version Drift**
   - Documented: fastapi:v2.0.0
   - Actual: fastapi:v2.0.1
   - Impact: Minor versioning inconsistency; potential behavioral differences
   - Root Cause: Auto-update or manual patch not reflected in docs

4. **PostgreSQL Image Version Drift**
   - Documented: postgres:15.0
   - Actual: postgres:14.0
   - Impact: Feature availability and compatibility differences
   - Root Cause: Downgrade not documented

#### 📝 Required Updates

**Option A: Update Implementation to Match Documentation** (Recommended)

```yaml
# docker-compose.yml changes
services:
  api:
    image: fastapi:v2.0.0 # Downgrade to documented version
    ports:
      - "8000:8000" # Change port to documented value
    environment:
      NODE_ENV: production # Fix to documented environment

  database:
    image: postgres:15.0 # Upgrade to documented version
```

**Option B: Update Documentation to Match Implementation** (If intentional)

```markdown
# Updated README.md

## Services

### API Service

- Port: 8001
- Image: fastapi:v2.0.1
- Environment: NODE_ENV=staging
- Note: Using staging environment for testing purposes

### Database (PostgreSQL)

- Port: 5432
- Image: postgres:14.0
- Note: Downgraded for compatibility with existing scripts
```

#### ✅ Recommendations

1. **Immediate Action**: Align API port and environment to production specs (High priority items)
2. **Version Strategy**: Establish a version pinning policy - should documented version be minimum supported or exact match?
3. **Documentation Process**: Update README before deploying Docker Compose changes
4. **Automation**: Add validation script to CI/CD that checks docker-compose.yml against documented specs
5. **Changelog**: Document why any deviations from spec exist (technical debt tracking)

#### 🔧 Prevention Measures

```bash
# Suggested validation script (docker-compose-validator.sh)
#!/bin/bash

# Check that all documented services exist in docker-compose
# Check that all ports match documentation
# Check that all image versions match or have documented reasons

# Run before commit
./validate-compose.sh docker-compose.yml README.md
```

## Context

This example demonstrates:

- Identifying version drift between documentation and implementation
- Port mapping mismatches with real consequences
- Environment configuration inconsistencies
- Prioritizing discrepancies by severity
- Providing clear remediation paths
- Distinguishing between documentation issues and implementation issues

## Effectiveness

- **Issues Identified**: ✓ 4 discrepancies found and categorized
- **Severity Prioritized**: ✓ High-impact items highlighted
- **Actionable**: ✓ Clear resolution paths provided
- **Prevention**: ✓ Recommendations for avoiding future drift

**Notes**: This validation ensures that documentation serves as the reliable single source of truth, preventing confusion and runtime failures caused by undocumented configuration changes.
