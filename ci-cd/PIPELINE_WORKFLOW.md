# CI/CD Pipeline Workflow - 25RP19452-NIYONKURU

## Overview

This document describes the comprehensive CI/CD pipeline for the Campus IT Helpdesk Ticket Microservice. The pipeline ensures consistent use of the identifier `25RP19452-NIYONKURU` across all stages.

**Project Identifier:** `25RP19452-NIYONKURU`

---

## Pipeline Architecture

### 7 Automated Stages

```
┌──────────────────────────────────────────────────────────────────────┐
│                      CI/CD PIPELINE WORKFLOW                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  STAGE 1: CODE VALIDATION         (Validate structure & identifier)  │
│       ↓                                                               │
│  STAGE 2: UNIT TESTS              (Run pytest with coverage)         │
│       ↓                                                               │
│  STAGE 3: DOCKER BUILD            (Build image, push to registry)    │
│       ↓                                                               │
│  STAGE 4: SECURITY SCANNING       (Trivy, SAST, secrets scan)        │
│       ↓                                                               │
│  STAGE 5: DEPLOY TO STAGING       (K8s deployment on develop branch) │
│       ↓                                                               │
│  STAGE 6: DEPLOY TO PRODUCTION    (K8s deployment on master branch)  │
│       ↓                                                               │
│  STAGE 7: MONITORING & ALERTS     (Health checks, notifications)     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Stage Details

### Stage 1: Code Validation

**Purpose:** Validate repository structure and verify consistent identifier usage

**Identifier Usage:**
- Validates `docker-compose.yml` contains `25RP19452-NIYONKURU`
- Validates `kubernetes/` manifests contain `25rp19452-niyonkuru`
- Ensures all required directories exist

**Outputs:**
- ✓ Project structure validated
- ✓ Identifier consistency verified

---

### Stage 2: Unit Tests & Coverage

**Purpose:** Run comprehensive test suite with coverage reporting

**Environment Variables:**
```yaml
PROJECT_ID: 25RP19452-NIYONKURU
PROJECT_ID_LOWER: 25rp19452-niyonkuru
KUBE_NAMESPACE: 25rp19452-niyonkuru
```

**Test Commands:**
```bash
pytest tests/ -v --tb=short --cov=src --cov-report=xml --cov-report=html
```

**Artifacts:**
- `coverage.xml` – Coverage report
- `htmlcov/` – HTML coverage report
- `test-results-25RP19452-NIYONKURU` – Packaged results

**Success Criteria:**
- All tests pass
- Coverage > 80%
- No test failures

---

### Stage 3: Docker Build & Push

**Purpose:** Build container image and push to registry

**Image Naming Convention:**
```
ghcr.io/25rp19452-niyonkuru/helpdesk:<build-number>
ghcr.io/25rp19452-niyonkuru/helpdesk:latest
```

**Dockerfile Labels:**
```dockerfile
org.opencontainers.image.title=Campus IT Helpdesk
org.opencontainers.image.description=Microservice for 25RP19452-NIYONKURU
org.opencontainers.image.version=1.0.0
```

**Build Metadata:**
- Identifier: `25RP19452-NIYONKURU`
- Image: `25rp19452-niyonkuru/helpdesk`
- Registry: `ghcr.io`

---

### Stage 4: Security Scanning

**Purpose:** Identify vulnerabilities and potential security issues

**Security Checks:**
1. **Trivy Filesystem Scan** – Scans all files for vulnerabilities
2. **SAST Analysis** – Static Application Security Testing
3. **Secrets Detection** – Finds exposed credentials
4. **Dependency Audit** – Checks Python packages for known CVEs

**Reports:**
- Trivy SARIF report
- GitHub Security dashboard integration
- Artifacts: `security-scan-25RP19452-NIYONKURU`

---

### Stage 5: Deploy to Staging

**Trigger:** `develop` branch or manual workflow dispatch

**Environment:**
```yaml
KUBE_NAMESPACE: 25rp19452-niyonkuru
APP_NAME: helpdesk-app
ENVIRONMENT: staging
```

**Deployment Steps:**
1. Apply Kubernetes namespace: `kubernetes/namespace.yaml`
2. Deploy application: `kubectl apply -f kubernetes/ -n 25rp19452-niyonkuru`
3. Set image: `kubectl set image deployment/helpdesk-app ...`
4. Wait for rollout: `kubectl rollout status deployment/helpdesk-app`

**Verification:**
- Pod status checks
- Endpoint health verification
- Service connectivity tests

---

### Stage 6: Deploy to Production

**Trigger:** `master` or `main` branch push

**Environment:**
```yaml
KUBE_NAMESPACE: 25rp19452-niyonkuru
APP_NAME: helpdesk-app
ENVIRONMENT: production
```

**Pre-deployment Checks:**
- Code review status: approved
- All tests: passed
- Security scan: passed
- Image verification: completed

**Deployment Commands:**
```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/ -n 25rp19452-niyonkuru
kubectl set image deployment/helpdesk-app helpdesk-app=<image> -n 25rp19452-niyonkuru
kubectl rollout status deployment/helpdesk-app -n 25rp19452-niyonkuru
```

**Deployment Record:**
- Project: `25RP19452-NIYONKURU`
- Version: `1.0.0`
- Commit: `${{ github.sha }}`
- Timestamp: `$(date -u +'%Y-%m-%dT%H:%M:%SZ')`

---

### Stage 7: Monitoring & Health Checks

**Purpose:** Verify application health and operational status

**Health Check Endpoints:**
- `GET /health` – Basic application health
- `GET /api/v1/health` – Detailed service health
- `GET /api/v1/tickets` – API functionality test

**Monitoring Points:**
- Namespace: `25rp19452-niyonkuru`
- Service: `25RP19452-NIYONKURU`
- Deployment: `helpdesk-app`

**Artifacts Generated:**
- `deployment-report-25RP19452-NIYONKURU`
- `pipeline-artifacts-25RP19452-NIYONKURU`

---

## Identifier Usage Across Pipeline

### Environment Variables

```yaml
# Global Configuration
PROJECT_ID: 25RP19452-NIYONKURU
PROJECT_ID_LOWER: 25rp19452-niyonkuru
KUBE_NAMESPACE: 25rp19452-niyonkuru
IMAGE_NAME: 25rp19452-niyonkuru/helpdesk
APP_NAME: helpdesk-app
```

### Repository Names

- **GitHub Repo:** `25RP19452-NIYONKURU`
- **Docker Registry:** `ghcr.io/25rp19452-niyonkuru/helpdesk`
- **K8s Namespace:** `25rp19452-niyonkuru`

### Pipeline Names

- **GitHub Actions:** `Campus IT Helpdesk CI/CD Pipeline - 25RP19452-NIYONKURU`
- **Pipeline Prefix:** All artifacts prefixed with `25RP19452-NIYONKURU`

### Kubernetes Resources

```yaml
# namespace.yaml
metadata:
  name: 25rp19452-niyonkuru

# deployment.yaml
labels:
  app: helpdesk-app
  project: 25rp19452-niyonkuru

# service.yaml
name: helpdesk-service
namespace: 25rp19452-niyonkuru
```

### Monitoring & Dashboards

- **Prometheus Label:** `project="25rp19452-niyonkuru"`
- **Grafana Dashboard:** `Campus IT Helpdesk - 25RP19452-NIYONKURU`
- **Loki Log Label:** `project_id=25rp19452-niyonkuru`

---

## Artifact Management

### Test Results
- Location: `test-results-25RP19452-NIYONKURU`
- Contains: `coverage.xml`, `htmlcov/`
- Retention: 90 days

### Build Artifacts
- Location: `docker-builds-25RP19452-NIYONKURU`
- Contains: Docker image metadata, build logs
- Retention: 30 days

### Deployment Reports
- Location: `deployment-report-25RP19452-NIYONKURU`
- Contains: Deployment logs, status, timestamps
- Retention: 365 days

### Security Scans
- Location: `security-scan-25RP19452-NIYONKURU`
- Contains: Trivy SARIF, vulnerability reports
- Retention: 365 days

---

## Branching Strategy

### Develop Branch → Staging
```
develop → [Test, Build, Deploy to Staging]
```

### Master/Main Branch → Production
```
master/main → [Test, Build, Security, Deploy to Production]
```

### Pull Requests
```
feature/* → [Test, Build, Security Check]
```

---

## Triggering the Pipeline

### Automatic Triggers
- Push to `master`, `main`, or `develop`
- Pull request to `master` or `main`

### Manual Triggers
```bash
# Workflow dispatch with environment selection
gh workflow run github-actions-pipeline.yml -f environment=production
```

---

## Pipeline Status Monitoring

### GitHub Actions Dashboard
1. Navigate to repository
2. Click "Actions" tab
3. Select `Campus IT Helpdesk CI/CD Pipeline - 25RP19452-NIYONKURU`
4. View workflow runs and logs

### Artifact Downloads
- All artifacts prefixed with: `25RP19452-NIYONKURU`
- Available for 90 days post-run

---

## Troubleshooting

### Common Issues

**Issue:** Test failures
- **Solution:** Check logs in `test-results-25RP19452-NIYONKURU`

**Issue:** Docker build fails
- **Solution:** Verify Dockerfile and docker-compose.yml use correct identifier

**Issue:** Deployment fails
- **Solution:** Verify K8s namespace `25rp19452-niyonkuru` exists

**Issue:** Security scan findings
- **Solution:** Review `security-scan-25RP19452-NIYONKURU` artifact

---

## Compliance & Verification

### Identifier Consistency Checklist

- [x] Repository name: `25RP19452-NIYONKURU`
- [x] Docker image: `25rp19452-niyonkuru/helpdesk`
- [x] K8s namespace: `25rp19452-niyonkuru`
- [x] CI/CD pipeline: `25RP19452-NIYONKURU`
- [x] Artifacts: Prefixed with `25RP19452-NIYONKURU`
- [x] Monitoring: Uses identifier labels
- [x] Documentation: References identifier consistently

---

## References

- GitHub Actions: `ci-cd/github-actions-pipeline.yml`
- GitLab CI: `ci-cd/.gitlab-ci.yml`
- Kubernetes: `kubernetes/`
- Docker: `docker/Dockerfile`, `docker-compose.yml`

**Last Updated:** December 19, 2025  
**Project:** Campus IT Helpdesk Ticket Microservice  
**Identifier:** 25RP19452-NIYONKURU
