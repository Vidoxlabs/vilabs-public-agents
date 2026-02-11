# Infrastructure Architect Agent

A specialized infrastructure-as-code (IaC) authority designed to validate orchestration logic, service discovery patterns, and container security.

## 🎯 Purpose

This agent acts as a senior site reliability engineer (SRE), reviewing configuration files (Docker Compose, Terraform, Kubernetes Manifests) to ensure they adhere to:

- **Service Discovery patterns** (using DNS over IPs)
- **Immutable Infrastructure principles**
- **Secret Management best practices** (environment injection)

## 🛠️ Capabilities

- **Topology Validation**: Detects circular dependencies and deployment order issues.
- **Pattern Enforcement**: Flags hardcoded IPs, missing health checks, or privileged containers.
- **Migration Assistance**: Helps refactor legacy monolithic configs into microservice patterns.

## 📦 Usage

**System Prompt Injection:**
Load the content of `agent.md` into your LLM's system context.

**Task Example:**

> "Review this docker-compose.yml for production readiness. Focus on service discovery and secret handling."

## 🏷️ Metadata

- **Confidence**: 0.92
- **Context**: DevOps, SRE, Docker, Kubernetes
