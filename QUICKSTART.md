# Quick Start Guide - Campus IT Helpdesk Ticket Microservice

**Project ID:** 25RP19452-NIYONKURU  
**Quick Reference Guide**

---

## 1. LOCAL DEVELOPMENT (Docker Compose)

### Start Application

```bash
cd /home/vboxuser/25RP19452_NIYONKURU_IT_HELP_DESK/25RP19452-NIYONKURU

# Start all services
docker-compose up -d

# Verify running
docker ps | grep 25RP19452

# Check logs
docker-compose logs -f helpdesk-app
```

### Test Application

```bash
# Health check
curl http://localhost:5000/health

# Create ticket
curl -X POST http://localhost:5000/api/v1/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Network issue",
    "description": "Cannot access lab",
    "category": "network",
    "priority": "high",
    "submitter_email": "student@university.edu",
    "submitter_name": "John Doe"
  }'

# List tickets
curl http://localhost:5000/api/v1/tickets

# Get metrics
curl http://localhost:5000/api/v1/metrics

# Stop services
docker-compose down
```

---

## 2. AUTOMATED DEPLOYMENT

### Full Infrastructure Setup

```bash
cd /home/vboxuser/25RP19452_NIYONKURU_IT_HELP_DESK/25RP19452-NIYONKURU

# Run complete deployment
./automation/deploy.sh

# This will:
# - Check prerequisites
# - Initialize Git
# - Build Docker image
# - Run tests
# - Start containers
# - Verify health
# - Create sample data
```

### Health Monitoring

```bash
# Monitor application
./automation/health-check.sh

# Output includes:
# - API health status
# - System metrics
# - Container status
# - Pod information
# - Health report
```

### Database Backup

```bash
# Create backup
./automation/backup.sh

# Restores:
# - Database backup
# - Log archives
# - Auto-cleanup old backups
```

---

## 3. KUBERNETES DEPLOYMENT

### Prerequisites

```bash
# Ensure Kubernetes is running
kubectl cluster-info

# Or use minikube
minikube start
```

### Deploy to Kubernetes

```bash
cd /home/vboxuser/25RP19452_NIYONKURU_IT_HELP_DESK/25RP19452-NIYONKURU

# Deploy application
./automation/k8s-deploy.sh

# This will:
# - Create namespace
# - Deploy storage
# - Configure RBAC
# - Deploy application (3 replicas)
# - Deploy services
# - Deploy monitoring
```

### Verify Kubernetes Deployment

```bash
# Check pods
kubectl get pods -n 25rp19452-niyonkuru

# Check services
kubectl get svc -n 25rp19452-niyonkuru

# Check deployment
kubectl get deployment -n 25rp19452-niyonkuru

# View pod logs
kubectl logs -n 25rp19452-niyonkuru -l app=helpdesk -f

# Port forward
kubectl port-forward -n 25rp19452-niyonkuru svc/helpdesk-service 8080:80
# Visit: http://localhost:8080
```

---

## 4. TESTING

### Run Unit Tests

```bash
cd /home/vboxuser/25RP19452_NIYONKURU_IT_HELP_DESK/25RP19452-NIYONKURU

# Install dependencies
pip install -r requirements.txt pytest pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Test Coverage

- ✓ Health endpoints
- ✓ Ticket creation
- ✓ Input validation
- ✓ Ticket retrieval
- ✓ Ticket updates
- ✓ Metrics collection
- ✓ Error handling

---

## 5. MONITORING ACCESS

### Local Deployment

```bash
# Prometheus (if running in Kubernetes)
kubectl port-forward -n 25rp19452-niyonkuru svc/prometheus-service 9090:9090
# Visit: http://localhost:9090

# Grafana
kubectl port-forward -n 25rp19452-niyonkuru svc/grafana-service 3000:3000
# Visit: http://localhost:3000
# Username: admin
# Password: admin
```

---

## 6. API ENDPOINTS REFERENCE

### Health Checks
```
GET /health                          # Application health
GET /api/v1/health                   # API health + database status
```

### Ticket Management
```
POST   /api/v1/tickets               # Create new ticket
GET    /api/v1/tickets               # List all tickets
GET    /api/v1/tickets?status=open   # Filter by status
GET    /api/v1/tickets?category=network   # Filter by category
GET    /api/v1/tickets/{id}          # Get specific ticket
PUT    /api/v1/tickets/{id}          # Update ticket
```

### Metrics
```
GET    /api/v1/metrics               # System metrics
```

---

## 7. CONFIGURATION

### Categories
- network
- login
- lab_computers
- software
- hardware
- other

### Priorities
- low
- medium
- high
- critical

### Statuses
- open
- in_progress
- resolved
- closed

---

## 8. DIRECTORY STRUCTURE

```
25RP19452-NIYONKURU/
├── src/app.py                       # Main application
├── tests/test_app.py                # Unit tests
├── docker/Dockerfile                # Container image
├── docker-compose.yml               # Local setup
├── kubernetes/                      # K8s manifests
├── ci-cd/                          # CI/CD pipelines
├── monitoring/                      # Monitoring configs
├── automation/                      # Automation scripts
├── requirements.txt                 # Dependencies
├── README.md                        # Full documentation
├── TECHNICAL_REPORT.md              # Technical details
└── DECLARATION_OF_ORIGINALITY.md    # Originality declaration
```

---

## 9. TROUBLESHOOTING

### Container not starting
```bash
# Check logs
docker-compose logs helpdesk-app

# Verify image built
docker images | grep 25rp19452-niyonkuru

# Rebuild image
docker build -f docker/Dockerfile -t 25rp19452-niyonkuru/helpdesk:latest .
```

### Port already in use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process or use different port
docker-compose -f docker-compose.yml down
```

### Database errors
```bash
# Check database file
ls -la /mnt/data/helpdesk/tickets.db

# Restore from backup
./automation/backup.sh restore /path/to/backup.db

# Check database
sqlite3 /mnt/data/helpdesk/tickets.db ".tables"
```

### Kubernetes pod won't start
```bash
# Check pod details
kubectl describe pod <pod-name> -n 25rp19452-niyonkuru

# Check events
kubectl get events -n 25rp19452-niyonkuru

# Check logs
kubectl logs <pod-name> -n 25rp19452-niyonkuru --previous
```

---

## 10. COMMON TASKS

### View Application Logs
```bash
# Docker Compose
docker-compose logs -f helpdesk-app

# Kubernetes
kubectl logs -n 25rp19452-niyonkuru -l app=helpdesk -f
```

### Scale Application
```bash
# Kubernetes only
kubectl scale deployment helpdesk-app --replicas=5 -n 25rp19452-niyonkuru
```

### Update Application
```bash
# Update code, then:
docker build -f docker/Dockerfile -t 25rp19452-niyonkuru/helpdesk:latest .
docker-compose up -d

# Or for Kubernetes:
kubectl rollout restart deployment/helpdesk-app -n 25rp19452-niyonkuru
```

### Check Resource Usage
```bash
# Docker
docker stats 25RP19452-NIYONKURU-helpdesk

# Kubernetes
kubectl top pods -n 25rp19452-niyonkuru
```

---

## 11. CLEAN UP

### Remove Docker Resources
```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi 25rp19452-niyonkuru/helpdesk:latest

# Clean volumes
docker volume rm $(docker volume ls | grep helpdesk | awk '{print $2}')
```

### Remove Kubernetes Resources
```bash
# Delete namespace (removes all resources in it)
kubectl delete namespace 25rp19452-niyonkuru

# Or selectively delete
kubectl delete -f kubernetes/ -n 25rp19452-niyonkuru
```

---

## 12. DOCUMENTATION FILES

| File | Purpose |
|------|---------|
| README.md | Project overview and detailed guide |
| TECHNICAL_REPORT.md | Comprehensive technical documentation |
| DECLARATION_OF_ORIGINALITY.md | Academic integrity declaration |
| docs/TECHNICAL_REPORT.md | Duplicate of technical report |

---

## 13. SUPPORT & CONTACT

For issues:
1. Check logs using commands above
2. Review README.md for detailed information
3. Check TECHNICAL_REPORT.md for architecture details
4. Verify configuration files in kubernetes/

---

**Quick Start Complete!**

For more information, see:
- `README.md` - Full project documentation
- `TECHNICAL_REPORT.md` - Technical architecture and implementation details
- Automation scripts in `automation/` directory

**Project Status:** ✓ Ready for deployment and assessment

---

*Last Updated: December 19, 2025*  
*Project ID: 25RP19452-NIYONKURU*
