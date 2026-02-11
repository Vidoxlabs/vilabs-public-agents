# Example: Docker Compose Validation for Production

## Input

A Docker Compose configuration for a microservice application that needs validation for production readiness.

**Current Configuration** (`docker-compose.yml`):

```yaml
version: "3.8"

services:
  api:
    image: myapp:latest
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_USER=admin
      - DB_PASSWORD=my_secret_pass_2024
      - REDIS_HOST=10.0.0.5
    volumes:
      - ./config:/app/config
      - /secrets/api:/app/secrets

  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=postgres123
    volumes:
      - db_data:/var/lib/postgresql/data

  redis:
    image: redis:7.0
    ports:
      - "6379:6379"
    command: redis-server

volumes:
  db_data:
```

## Output

### 🏗️ Infrastructure Review Report

**Component**: Microservice Stack
**Type**: Docker Compose
**Environment**: Production (Intended)
**Status**: ❌ Not Production Ready

#### Security & Resilience Analysis

| Analysis          | Status    | Notes                        |
| ----------------- | --------- | ---------------------------- |
| Service Discovery | ❌ Failed | Hardcoded IP for Redis       |
| Secret Management | ❌ Failed | Embedded passwords in config |
| Resource Limits   | ❌ Failed | No CPU/memory limits         |
| Health Checks     | ❌ Failed | Missing health checks        |
| Security Context  | ❌ Failed | Running as root              |
| Networking        | ❌ Failed | Exposed ports, no encryption |

#### ⚠️ Critical Findings

**Critical** 🔴

1. **Embedded Secrets in Configuration**
   - **Location**: Lines 10-12, 24-25
   - **Issue**: Hardcoded passwords visible in plain text
   - **Impact**: Secret exposure to anyone with access to file; will be committed to Git
   - **Remediation**: Use environment file or secret management system

2. **Hardcoded IP Address**
   - **Location**: Line 13 (`REDIS_HOST=10.0.0.5`)
   - **Issue**: Direct IP reference breaks service discovery pattern
   - **Impact**: Scaling or rearrangement requires manual config change
   - **Remediation**: Use service name (`redis`) or DNS service discovery

3. **Missing Health Checks**
   - **Location**: All services
   - **Issue**: No liveness or readiness probes
   - **Impact**: Docker doesn't know if services are healthy; orchestrators can't restart failed services
   - **Remediation**: Add `healthcheck` block to each service

4. **No Resource Limits**
   - **Location**: All services
   - **Issue**: Services can consume unlimited CPU/memory
   - **Impact**: "Noisy neighbor" problem; one service can crash others
   - **Remediation**: Define `cpu_shares`, `mem_limit`, `memswap_limit`

**High** 🟠

5. **Running as Root User**
   - **Location**: All services
   - **Issue**: Default container entrypoint runs as root (UID 0)
   - **Impact**: Compromised container has full system access
   - **Remediation**: Specify non-root user in Dockerfile or Docker Compose

6. **Direct Port Exposure**
   - **Location**: Lines 7, 21, 31
   - **Issue**: Database and cache ports exposed to network
   - **Impact**: External systems can access database directly
   - **Remediation**: Remove port mappings for internal services; only expose API port

7. **No Restart Policy**
   - **Location**: All services
   - **Issue**: Failed containers won't automatically restart
   - **Impact**: Manual intervention required for service recovery
   - **Remediation**: Add `restart_policy` or `restart: unless-stopped`

**Medium** 🟡

8. **Using Latest Image Tag**
   - **Location**: Line 5
   - **Issue**: `myapp:latest` is unpredictable; can't guarantee reproducibility
   - **Impact**: Different versions could run in different environments
   - **Remediation**: Pin specific version tags: `myapp:1.2.3`

9. **File Mounts from Host**
   - **Location**: Line 9-10
   - **Issue**: Mounting local directories breaks immutable infrastructure principle
   - **Impact**: Configuration inconsistency across deployments
   - **Remediation**: Embed config in image or inject via environment variables

#### ✅ Corrected Configuration

```yaml
version: "3.8"

networks:
  app-network:
    driver: bridge

volumes:
  db_data:

services:
  api:
    image: myapp:1.2.3 # ✅ Pinned version
    container_name: api
    user: "1000:1000" # ✅ Non-root user
    restart: unless-stopped # ✅ Auto-restart
    healthcheck: # ✅ Health checks
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    ports:
      - "8000:8000" # ✅ Only API port exposed
    networks:
      - app-network
    environment:
      - DB_HOST=postgres # ✅ Service name instead of IP
      - DB_PORT=5432
      - LOG_LEVEL=${LOG_LEVEL:-info}
      - REDIS_HOST=redis # ✅ Service name
      - REDIS_PORT=6379
    # ✅ Secrets injected from external file
    env_file:
      - .env.production
    resources: # ✅ Resource limits defined
      requests:
        cpus: "0.5"
        memory: 512M
      limits:
        cpus: "1"
        memory: 1G
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  postgres:
    image: postgres:15.2 # ✅ Pinned version
    container_name: postgres
    user: "999:999" # ✅ Non-root user
    restart: unless-stopped
    healthcheck: # ✅ Health checks
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network
    # ✅ Secrets from environment file
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB:-myapp}
    volumes:
      - db_data:/var/lib/postgresql/data
    # ✅ No port exposure for internal service
    resources:
      requests:
        cpus: "0.25"
        memory: 256M
      limits:
        cpus: "0.5"
        memory: 512M

  redis:
    image: redis:7.0.10 # ✅ Pinned version
    container_name: redis
    user: "999:999" # ✅ Non-root user
    restart: unless-stopped
    healthcheck: # ✅ Health checks
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - app-network
    command:
      - redis-server
      - "--requirepass"
      - "${REDIS_PASSWORD}" # ✅ Password from environment
      - "--save"
      - "60"
      - "1000"
    # ✅ No port exposure for internal service
    resources:
      requests:
        cpus: "0.1"
        memory: 128M
      limits:
        cpus: "0.25"
        memory: 256M
```

**Environment File** (`.env.production` - not committed):

```env
LOG_LEVEL=info
POSTGRES_USER=appuser
POSTGRES_PASSWORD=<generated-secure-password>
POSTGRES_DB=myapp_prod
REDIS_PASSWORD=<generated-secure-password>
```

#### 📋 Key Improvements

| Issue                 | Before           | After                       |
| --------------------- | ---------------- | --------------------------- |
| Secrets               | Embedded in file | External `.env` file        |
| Service Communication | Hardcoded IP     | DNS service names           |
| Health Checks         | None             | Defined for all services    |
| Resource Limits       | None             | CPU and memory bounds       |
| User Context          | root (UID 0)     | Non-root users              |
| Port Exposure         | All exposed      | Only API public             |
| Image Tags            | `latest`         | Pinned versions             |
| Restart Policy        | Manual only      | Auto-restart enabled        |
| Dependencies          | None             | Explicit with health checks |

#### 💡 Additional Recommendations

1. **SSL/TLS**: Add reverse proxy (nginx) with TLS termination for API
2. **Logging**: Configure Docker logging driver (json-file with rotation)
3. **Monitoring**: Add Prometheus endpoint for metrics collection
4. **Backup**: Define backup strategy for database volumes
5. **CI/CD Integration**: Automate image building and scanning
6. **Secret Rotation**: Implement regular credential rotation
7. **Network Segmentation**: Use overlay networks for multi-host deployment

#### 🚀 Next Steps for Production

- [ ] Generate secure passwords (use `openssl rand -base64 32`)
- [ ] Create `.env.production` from template
- [ ] Scan images for vulnerabilities with Trivy/Anchore
- [ ] Test health checks manually
- [ ] Load test resource limits
- [ ] Set up Docker registry authentication
- [ ] Enable Docker content trust for image signing
- [ ] Implement secret rotation workflow

## Context

This example demonstrates:

- Identifying embedded secrets and security risks
- Service discovery pattern validation
- Health check implementation
- Resource management and limits
- Production-readiness standards
- Clear migration path from development to production

## Effectiveness

- **Issues Identified**: ✓ 9 critical and high-priority issues
- **Security Improved**: ✓ Secrets externalized, non-root users
- **Operational Ready**: ✓ Health checks and restart policies
- **Scalability**: ✓ Service discovery enables horizontal scaling

**Notes**: This refactored configuration is production-ready, secure, and follows infrastructure-as-code best practices. Regular reviews and updates as the application scales are essential.
