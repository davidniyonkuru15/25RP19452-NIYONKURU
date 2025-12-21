# Campus IT Helpdesk Microservice - Technical Report

**Project ID:** 25RP19452-NIYONKURU  
**Student:** Niyonkuru (25RP19452)  
**Date:** December 21, 2025

---

## 1. Introduction
This report documents the complete DevOps lifecycle implementation of the Campus IT Helpdesk Microservice, covering infrastructure, CI/CD, containerization, orchestration, monitoring, automation, and evidence of originality.

## 2. Project Overview
- **Microservice:** Python Flask REST API for IT ticket management
- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes (minikube)
- **CI/CD:** GitHub Actions, GitLab CI/CD
- **Monitoring:** Prometheus, Grafana, Loki
- **Automation:** Shell scripts for deployment, backup, and health checks

## 3. Infrastructure & VM Setup
- VirtualBox VM running Linux OS
- Docker, kubectl, and minikube installed
- Network configured for SSH and internet access
- Resource allocation: 2+ CPUs, 4GB+ RAM, 20GB+ disk

## 4. Version Control & Git Workflow
- Git repository initialized and connected to remote
- Feature branching and PR workflow followed
- Commit messages are meaningful and grouped logically
- Merge conflicts resolved via PRs

## 5. CI/CD Pipeline
- GitHub Actions and GitLab CI/CD pipelines implemented
- Stages: Build, Test, Deploy
- Automated builds/tests on commit
- Secrets managed securely

## 6. Containerization & Registry
- Efficient Dockerfile using python:3.11-slim
- Images built, tagged, and pushed to Docker Hub and GHCR
- .dockerignore used to exclude unnecessary files

## 7. Deployment & Automation
- Kubernetes manifests for deployment, service, HPA, storage, RBAC, configmap, namespace
- Automated deployment via shell scripts
- HPA enables scaling from 3 to 10 pods
- Backup and restore scripts provided

## 8. Monitoring & Reliability
- Prometheus scrapes /metrics endpoint from helpdesk-app
- Grafana dashboards visualize metrics
- Loki aggregates logs
- Health checks via liveness/readiness probes
- Prometheus alert rules configured

## 9. Testing & Quality
- Unit tests implemented in `tests/test_app.py`
- All tests pass successfully

## 10. Documentation & Evidence
- README, quickstart, technical report, and verification checklist included
- Evidence folder contains screenshots, logs, and configuration files

## 11. Originality Declaration
- Unique identifier used throughout: 25RP19452-NIYONKURU
- Signed declaration of originality included

## 12. Conclusion
All assessment requirements have been met, and the project is ready for submission. Please refer to the evidence file for screenshots, logs, and configuration details.

---

**End of Technical Report**
