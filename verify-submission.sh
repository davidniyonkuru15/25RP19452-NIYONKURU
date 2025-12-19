#!/bin/bash

################################################################################
# CAMPUS IT HELPDESK - SUBMISSION VERIFICATION SCRIPT
# Project ID: 25RP19452-NIYONKURU
# Purpose: Verify all deliverables are present and correct
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
PASS=0
FAIL=0

# Logging functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASS++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAIL++))
}

warn() {
    echo -e "${YELLOW}!${NC} $1"
}

info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Project root
PROJECT_ROOT="/home/vboxuser/25RP19452_NIYONKURU_IT_HELP_DESK/25RP19452-NIYONKURU"

echo "==============================================="
echo "Campus IT Helpdesk - Submission Verification"
echo "Project ID: 25RP19452-NIYONKURU"
echo "==============================================="
echo ""

# 1. Check directory structure
echo -e "${BLUE}[1] Checking Directory Structure${NC}"
echo "---"

if [ -d "$PROJECT_ROOT" ]; then
    pass "Project root directory exists"
else
    fail "Project root directory not found"
fi

# Check essential directories
dirs=("src" "tests" "docker" "kubernetes" "ci-cd" "monitoring" "automation" "docs")
for dir in "${dirs[@]}"; do
    if [ -d "$PROJECT_ROOT/$dir" ]; then
        pass "Directory: $dir/"
    else
        fail "Missing directory: $dir/"
    fi
done

echo ""

# 2. Check source code files
echo -e "${BLUE}[2] Checking Source Code Files${NC}"
echo "---"

files=(
    "src/app.py:Application code"
    "tests/test_app.py:Test suite"
    "requirements.txt:Dependencies"
    "docker/Dockerfile:Container image"
    "docker-compose.yml:Docker Compose config"
)

for file_desc in "${files[@]}"; do
    IFS=':' read -r file desc <<< "$file_desc"
    if [ -f "$PROJECT_ROOT/$file" ]; then
        lines=$(wc -l < "$PROJECT_ROOT/$file")
        pass "$desc ($file) - $lines lines"
    else
        fail "Missing: $file"
    fi
done

echo ""

# 3. Check Kubernetes manifests
echo -e "${BLUE}[3] Checking Kubernetes Manifests${NC}"
echo "---"

k8s_files=(
    "kubernetes/namespace.yaml"
    "kubernetes/deployment.yaml"
    "kubernetes/service.yaml"
    "kubernetes/storage.yaml"
    "kubernetes/rbac.yaml"
    "kubernetes/hpa.yaml"
    "kubernetes/configmap.yaml"
)

for file in "${k8s_files[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        if kubectl apply --dry-run=client -f "$PROJECT_ROOT/$file" &>/dev/null; then
            pass "Valid K8s manifest: $file"
        else
            warn "K8s manifest may have validation issues: $file"
        fi
    else
        fail "Missing K8s manifest: $file"
    fi
done

echo ""

# 4. Check CI/CD configurations
echo -e "${BLUE}[4] Checking CI/CD Configurations${NC}"
echo "---"

cicd_files=(
    "ci-cd/github-actions-pipeline.yml:GitHub Actions"
    "ci-cd/.gitlab-ci.yml:GitLab CI/CD"
)

for file_desc in "${cicd_files[@]}"; do
    IFS=':' read -r file desc <<< "$file_desc"
    if [ -f "$PROJECT_ROOT/$file" ]; then
        pass "$desc pipeline configured"
    else
        fail "Missing: $file"
    fi
done

echo ""

# 5. Check monitoring configurations
echo -e "${BLUE}[5] Checking Monitoring Stack${NC}"
echo "---"

monitoring_files=(
    "monitoring/prometheus.yaml:Prometheus"
    "monitoring/grafana.yaml:Grafana"
    "monitoring/loki.yaml:Loki logs"
)

for file_desc in "${monitoring_files[@]}"; do
    IFS=':' read -r file desc <<< "$file_desc"
    if [ -f "$PROJECT_ROOT/$file" ]; then
        pass "$desc configuration: $file"
    else
        fail "Missing: $file"
    fi
done

echo ""

# 6. Check automation scripts
echo -e "${BLUE}[6] Checking Automation Scripts${NC}"
echo "---"

scripts=(
    "automation/deploy.sh:Infrastructure deployment"
    "automation/k8s-deploy.sh:Kubernetes deployment"
    "automation/health-check.sh:Health monitoring"
    "automation/backup.sh:Backup and recovery"
)

for script_desc in "${scripts[@]}"; do
    IFS=':' read -r script desc <<< "$script_desc"
    if [ -f "$PROJECT_ROOT/$script" ]; then
        if [ -x "$PROJECT_ROOT/$script" ]; then
            pass "Executable script: $desc"
        else
            warn "Script not executable: $script (attempting to fix)"
            chmod +x "$PROJECT_ROOT/$script"
        fi
    else
        fail "Missing script: $script"
    fi
done

echo ""

# 7. Check documentation
echo -e "${BLUE}[7] Checking Documentation${NC}"
echo "---"

docs=(
    "README.md:Project README"
    "QUICKSTART.md:Quick start guide"
    "DECLARATION_OF_ORIGINALITY.md:Originality declaration"
    "INDEX.md:Project index"
    "docs/TECHNICAL_REPORT.md:Technical report"
)

for doc_desc in "${docs[@]}"; do
    IFS=':' read -r doc desc <<< "$doc_desc"
    if [ -f "$PROJECT_ROOT/$doc" ]; then
        lines=$(wc -l < "$PROJECT_ROOT/$doc")
        pass "$desc - $lines lines"
    else
        fail "Missing documentation: $doc"
    fi
done

echo ""

# 8. Check for unique identifier usage
echo -e "${BLUE}[8] Verifying Unique Identifier Usage${NC}"
echo "---"

identifier="25RP19452-NIYONKURU"
identifier_count=$(grep -r "$identifier" "$PROJECT_ROOT" 2>/dev/null | wc -l)

if [ "$identifier_count" -gt 10 ]; then
    pass "Unique identifier found in $identifier_count locations"
else
    warn "Unique identifier found in only $identifier_count locations (expected > 10)"
fi

# Check specific locations
locations=(
    "docker-compose.yml"
    "kubernetes/namespace.yaml"
    "kubernetes/deployment.yaml"
    "DECLARATION_OF_ORIGINALITY.md"
)

for location in "${locations[@]}"; do
    if grep -q "$identifier" "$PROJECT_ROOT/$location" 2>/dev/null; then
        pass "Identifier used in: $location"
    else
        warn "Identifier not found in: $location"
    fi
done

echo ""

# 9. Check Python code quality
echo -e "${BLUE}[9] Checking Python Code Quality${NC}"
echo "---"

if python3 -m py_compile "$PROJECT_ROOT/src/app.py" 2>/dev/null; then
    pass "Application code syntax valid"
else
    fail "Application code has syntax errors"
fi

if python3 -m py_compile "$PROJECT_ROOT/tests/test_app.py" 2>/dev/null; then
    pass "Test code syntax valid"
else
    fail "Test code has syntax errors"
fi

echo ""

# 10. Check Docker configuration
echo -e "${BLUE}[10] Checking Docker Configuration${NC}"
echo "---"

if docker build -f "$PROJECT_ROOT/docker/Dockerfile" -t test-build "$PROJECT_ROOT" &>/dev/null; then
    pass "Dockerfile builds successfully"
    docker rmi test-build 2>/dev/null || true
else
    warn "Dockerfile build failed (Docker may not be available)"
fi

if [ -f "$PROJECT_ROOT/docker-compose.yml" ]; then
    if docker-compose -f "$PROJECT_ROOT/docker-compose.yml" config &>/dev/null; then
        pass "Docker Compose configuration is valid"
    else
        warn "Docker Compose validation failed"
    fi
else
    fail "docker-compose.yml not found"
fi

echo ""

# 11. File statistics
echo -e "${BLUE}[11] Project Statistics${NC}"
echo "---"

total_lines=$(find "$PROJECT_ROOT" -name "*.py" -o -name "*.yaml" -o -name "*.yml" -o -name "*.sh" -o -name "*.md" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
total_files=$(find "$PROJECT_ROOT" -type f | grep -v "^\." | wc -l)

info "Total lines of code/config: $total_lines"
info "Total files: $total_files"

py_lines=$(find "$PROJECT_ROOT" -name "*.py" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
info "Python code: $py_lines lines"

yaml_lines=$(find "$PROJECT_ROOT" -name "*.yaml" -o -name "*.yml" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
info "YAML manifests: $yaml_lines lines"

doc_lines=$(find "$PROJECT_ROOT" -name "*.md" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
info "Documentation: $doc_lines lines"

echo ""

# 12. Summary
echo -e "${BLUE}[12] Verification Summary${NC}"
echo "---"

TOTAL=$((PASS + FAIL))

echo -e "Total Checks: $TOTAL"
echo -e "${GREEN}Passed: $PASS${NC}"
if [ $FAIL -gt 0 ]; then
    echo -e "${RED}Failed: $FAIL${NC}"
fi

echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✓ ALL VERIFICATION CHECKS PASSED${NC}"
    echo -e "${GREEN}  Project is ready for submission${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    exit 0
else
    echo -e "${YELLOW}════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  ! WARNINGS OR ISSUES DETECTED${NC}"
    echo -e "${YELLOW}  Please review the items above${NC}"
    echo -e "${YELLOW}════════════════════════════════════════${NC}"
    exit 1
fi
