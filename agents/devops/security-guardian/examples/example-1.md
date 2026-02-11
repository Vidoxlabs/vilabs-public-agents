# Example: Securing a Docker Compose Stack with Hardcoded Secrets

## Input

A Docker Compose configuration with multiple critical security vulnerabilities including hardcoded credentials, privileged containers, and unsafe volume mounts.

**Vulnerable Configuration** (docker-compose.yml):

```yaml
version: "3.8"

services:
  api:
    image: myapp:latest
    ports:
      - "0.0.0.0:8080:8080"
    privileged: true
    environment:
      - DATABASE_URL=postgresql://dbuser:P@ssw0rd123!@db:5432/main
      - REDIS_PASSWORD=redis_secret_key_abc123
      - JWT_SECRET=super_secret_jwt_key_12345
      - AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
      - AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /etc/passwd:/etc/passwd:ro
      - ./config:/app/config
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=postgres123
      - POSTGRES_DB=main
    volumes:
      - postgres_data:/var/lib/postgresql/data
    # No health check
    # No user specified (runs as root)

  redis:
    image: redis:7.0
    command: redis-server --requirepass redis_secret_key_abc123
    # No user specified
    # No capabilities restrictions

volumes:
  postgres_data:
```

**Security Scan Summary**:

- ❌ 5 hardcoded credentials
- ❌ Privileged container mode
- ❌ Docker socket mounted
- ❌ Running as root
- ❌ Overly broad port exposure
- ❌ No health checks
- ❌ Dangerous volume mounts

## Output

### 🔐 Security Audit Report

**Component**: Microservice Stack
**Type**: Docker Compose
**Audit Date**: 2026-02-06
**Status**: ❌ DEPLOYMENT BLOCKED

#### Security Scorecard

| Category            | Status | Issues      | Severity |
| ------------------- | ------ | ----------- | -------- |
| Secrets             | 🔴     | 5 hardcoded | Critical |
| Container Hardening | 🔴     | 3 issues    | Critical |
| Privileges          | 🔴     | 2 issues    | Critical |
| Network Security    | 🟡     | 1 issue     | High     |

#### 🚫 BLOCKING CRITICAL ISSUES

**1. Hardcoded Database Credentials** 🔴

- **Location**: `docker-compose.yml`, line 10
- **Violation**: `DATABASE_URL=postgresql://dbuser:P@ssw0rd123!@db:5432/main`
- **Risk**: Credentials exposed in configuration file; will be committed to Git
- **Impact**: Complete database compromise if repository is leaked
- **Remediation**:
  ```yaml
  environment:
    - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
  ```

**2. Hardcoded Redis Password** 🔴

- **Location**: `docker-compose.yml`, lines 11 and 25
- **Violation**: `REDIS_PASSWORD=redis_secret_key_abc123`
- **Risk**: Plain text password in configuration
- **Impact**: Redis cache compromise; potential data exposure
- **Remediation**:
  ```yaml
  environment:
    - REDIS_PASSWORD=${REDIS_PASSWORD}
  command: redis-server --requirepass ${REDIS_PASSWORD}
  ```

**3. Hardcoded JWT Secret** 🔴

- **Location**: `docker-compose.yml`, line 12
- **Violation**: `JWT_SECRET=super_secret_jwt_key_12345`
- **Risk**: Session/authentication compromise
- **Impact**: Anyone with this secret can forge valid authentication tokens
- **Remediation**:
  ```yaml
  environment:
    - JWT_SECRET=${JWT_SECRET}
  ```

**4. Exposed AWS Credentials** 🔴

- **Location**: `docker-compose.yml`, lines 13-14
- **Violation**: AWS Access Key ID and Secret Access Key hardcoded
- **Risk**: AWS account compromise; unauthorized resource access
- **Impact**: Attacker can access all AWS resources, incur massive charges, steal data
- **Remediation**:
  ```yaml
  environment:
    - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
    - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
  # OR use IAM roles if running on EC2/ECS
  ```

**5. Privileged Container Mode** 🔴

- **Location**: `docker-compose.yml`, line 7
- **Violation**: `privileged: true`
- **Risk**: Container has full kernel access, equivalent to root SSH
- **Impact**: Complete host compromise if container is exploited
- **Remediation**: Remove `privileged: true` and add specific capabilities needed
  ```yaml
  cap_drop:
    - ALL
  cap_add:
    - NET_BIND_SERVICE
  ```

**6. Docker Socket Mounting** 🔴

- **Location**: `docker-compose.yml`, line 16
- **Violation**: `/var/run/docker.sock:/var/run/docker.sock`
- **Risk**: Container can spawn other containers with full host access
- **Impact**: Complete host compromise; escape from container isolation
- **Remediation**: Remove. Use alternative: secure Docker API proxy or don't mount socket
  ```yaml
  # REMOVE THIS LINE
  # - /var/run/docker.sock:/var/run/docker.sock
  ```

**7. Running as Root User** 🔴

- **Location**: All services (no user specified)
- **Violation**: No `user:` directive; defaults to root (UID 0)
- **Risk**: Compromised container has UID 0 on host filesystem
- **Impact**: If container broken into, attacker has full access to volumes
- **Remediation**:
  ```yaml
  api:
    user: "1000:1000"
  db:
    user: "999:999"
  redis:
    user: "999:999"
  ```

#### ⚠️ High Priority Issues

**8. Overly Broad Port Exposure** 🟠

- **Location**: `docker-compose.yml`, line 8
- **Violation**: `- "0.0.0.0:8080:8080"` exposes to all interfaces
- **Risk**: API accessible from external networks
- **Remediation**: Expose only to localhost or specific network

  ```yaml
  # Option 1: Localhost only
  - "127.0.0.1:8080:8080"

  # Option 2: On internal network only (no port mapping)
  networks:
    - internal-network
  ```

**9. Missing Health Checks** 🟠

- **Location**: db and redis services
- **Violation**: No health check defined
- **Risk**: Container failures not detected; unhealthy services still receive traffic
- **Impact**: Application errors go undetected; manual recovery required
- **Remediation**:
  ```yaml
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
  ```

#### ✅ Corrected Secure Configuration

**docker-compose.yml** (Secured):

```yaml
version: "3.8"

networks:
  internal-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

services:
  api:
    image: myapp:1.2.3 # ✅ Pinned version
    user: "1000:1000" # ✅ Non-root user
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    ports:
      - "127.0.0.1:8080:8080" # ✅ Localhost only
    networks:
      - internal-network
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME} # ✅ Variables
      - REDIS_PASSWORD=${REDIS_PASSWORD} # ✅ Variables
      - JWT_SECRET=${JWT_SECRET} # ✅ Variables
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} # ✅ Variables
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} # ✅ Variables
    env_file:
      - .env.production # ✅ Secrets from file
    # ✅ No privileged mode
    # ✅ No Docker socket mount
    # ✅ Only safe volumes
    volumes:
      - ./config:/app/config:ro # ✅ Read-only
    cap_drop:
      - ALL # ✅ Drop all capabilities
    cap_add:
      - NET_BIND_SERVICE # ✅ Minimal needed capabilities
    read_only: true # ✅ Read-only root filesystem
    tmpfs:
      - /tmp # ✅ Temporary writable mount for logs
      - /run
    depends_on:
      db:
        condition: service_healthy # ✅ Explicit health dependency
      redis:
        condition: service_healthy

  db:
    image: postgres:15.2 # ✅ Pinned version
    user: "999:999" # ✅ Non-root user
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal-network
    environment:
      - POSTGRES_USER=${DB_USER} # ✅ Variables
      - POSTGRES_PASSWORD=${DB_PASSWORD} # ✅ Variables
      - POSTGRES_DB=${DB_NAME} # ✅ Variables
    volumes:
      - postgres_data:/var/lib/postgresql/data
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETUID
      - SETGID
    read_only: true
    tmpfs:
      - /run

  redis:
    image: redis:7.0.10 # ✅ Pinned version
    user: "999:999" # ✅ Non-root user
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - internal-network
    command:
      - redis-server
      - "--requirepass"
      - "${REDIS_PASSWORD}" # ✅ Variables
      - "--save"
      - "60"
      - "1000"
    volumes:
      - redis_data:/data
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp

volumes:
  postgres_data:
  redis_data:
```

**.env.template** (Committed to repo):

```bash
# Database Configuration
DB_USER=appuser
DB_PASSWORD=CHANGE_ME_generate_secure_password
DB_NAME=myapp

# Redis Configuration
REDIS_PASSWORD=CHANGE_ME_generate_secure_password

# JWT Configuration
JWT_SECRET=CHANGE_ME_generate_secure_random_string

# AWS Configuration
AWS_ACCESS_KEY_ID=CHANGE_ME
AWS_SECRET_ACCESS_KEY=CHANGE_ME
```

**.env.production** (NOT committed - generated for deployment):

```bash
DB_USER=prod_appuser
DB_PASSWORD=<generated-strong-password-here>
DB_NAME=myapp_prod
REDIS_PASSWORD=<generated-strong-password-here>
JWT_SECRET=<generated-random-secret-here>
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
```

**.gitignore** (Updated):

```bash
# Environment files (never commit)
.env
.env.local
.env.*.local

# Files that might contain credentials
config.local.json
secrets/
credentials/
```

#### 📋 Security Verification Checklist

- [ ] No `.env` or `.env.production` files in Git history
- [ ] All credentials use `${VARIABLE_NAME}` interpolation
- [ ] No `privileged: true` in any service
- [ ] No Docker socket mounts
- [ ] All services specify non-root `user:`
- [ ] All services have `healthcheck` defined
- [ ] `cap_drop: [ALL]` for all services
- [ ] Only necessary `cap_add` entries
- [ ] Root filesystem is `read_only: true`
- [ ] Temporary directories use `tmpfs:`
- [ ] Only API port exposed; database/cache internal only
- [ ] Base images pinned to specific versions
- [ ] Image scan passes (`trivy` or `grype`)
- [ ] `.gitignore` includes all credential files
- [ ] `.env.template` provides all required variables

#### 🔄 Deployment Procedure

1. **Generate Secrets**:

   ```bash
   cp .env.template .env.production
   # Edit .env.production with actual secrets
   openssl rand -base64 32  # For password generation
   ```

2. **Verify No Leaks**:

   ```bash
   git status  # Ensure .env.production is NOT listed
   git diff  # Verify no credentials in changes
   ```

3. **Scan Images**:

   ```bash
   docker-compose build
   trivy image myapp:1.2.3
   trivy image postgres:15.2
   trivy image redis:7.0.10
   ```

4. **Deploy**:

   ```bash
   docker-compose --env-file=.env.production up -d
   ```

5. **Verify Security**:
   ```bash
   docker exec api id  # Should show UID 1000, not 0
   docker ps --format "{{.Image}} {{.Status}}"  # All healthy
   ```

## Context

This example demonstrates:

- Identifying hardcoded credentials
- Removing privileged containers and dangerous mounts
- Implementing least-privilege user contexts
- Proper secret management with environment variables
- Health checks and dependency ordering
- Capability restrictions
- Read-only filesystems

## Effectiveness

**Before Audit**:

- 🔴 Critical vulnerabilities: 7
- 🟠 High severity: 2
- **Deployment Status**: BLOCKED

**After Remediation**:

- ✅ Critical vulnerabilities: 0
- ✅ High severity: 0
- **Deployment Status**: APPROVED

**Security Improvements**:

- No hardcoded credentials in Git
- Container compromise cannot access host system
- No privileged execution
- Full audit trail possible with health checks

**Notes**: This hardening transforms a critically vulnerable stack into a production-ready secure configuration. Regular security audits should continue as the application evolves.
