#!/bin/bash

#############################################################################
# Campus IT Helpdesk - Monitoring & Health Check Script
# Student ID: 25RP19452-NIYONKURU
# Purpose: Monitor application health and collect metrics
#############################################################################

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration
PROJECT_ID="25RP19452-NIYONKURU"
APP_URL="http://localhost:5000"
NAMESPACE="25rp19452-niyonkuru"
METRICS_FILE="/home/vboxuser/25RP19452_NIYONKURU_IT_HELP_DESK/logs/metrics.json"

# Create metrics directory
mkdir -p "$(dirname "$METRICS_FILE")"

# Monitor endpoint
monitor_endpoint() {
    local endpoint=$1
    local name=$2
    
    log_info "Checking ${name}..."
    
    if response=$(curl -s -w "\n%{http_code}" "${endpoint}" 2>/dev/null); then
        http_code=$(echo "$response" | tail -n1)
        body=$(echo "$response" | head -n-1)
        
        if [ "$http_code" = "200" ]; then
            log_success "${name} - HTTP ${http_code}"
            echo "$body"
        else
            log_error "${name} - HTTP ${http_code}"
        fi
    else
        log_error "${name} - Connection failed"
    fi
}

# Check application health
check_app_health() {
    log_info "========================================"
    log_info "Application Health Check"
    log_info "========================================"
    
    monitor_endpoint "${APP_URL}/health" "Health Check"
    monitor_endpoint "${APP_URL}/api/v1/health" "API Health"
}

# Get metrics
collect_metrics() {
    log_info "========================================"
    log_info "Collecting System Metrics"
    log_info "========================================"
    
    if response=$(curl -s "${APP_URL}/api/v1/metrics" 2>/dev/null); then
        echo "$response" | tee "$METRICS_FILE"
        log_success "Metrics collected and saved to ${METRICS_FILE}"
    else
        log_error "Failed to collect metrics"
    fi
}

# Check Docker containers
check_containers() {
    log_info "========================================"
    log_info "Docker Container Status"
    log_info "========================================"
    
    docker ps --filter "name=25RP19452"
}

# Check Kubernetes pods
check_k8s_pods() {
    log_info "========================================"
    log_info "Kubernetes Pod Status"
    log_info "========================================"
    
    if command -v kubectl &> /dev/null; then
        kubectl get pods -n "${NAMESPACE}" 2>/dev/null || log_warning "Kubernetes cluster not available"
    fi
}

# Monitor container logs
check_logs() {
    log_info "========================================"
    log_info "Recent Application Logs"
    log_info "========================================"
    
    if docker ps | grep -q "25RP19452"; then
        docker logs --tail=20 "25RP19452-NIYONKURU-helpdesk" 2>/dev/null || log_warning "Container logs not available"
    fi
}

# Generate report
generate_report() {
    local report_file="/home/vboxuser/25RP19452_NIYONKURU_IT_HELP_DESK/logs/health_report_$(date +%Y%m%d_%H%M%S).txt"
    
    log_info "Generating health report..."
    
    {
        echo "==============================================="
        echo "Campus IT Helpdesk - Health Report"
        echo "Project ID: ${PROJECT_ID}"
        echo "Generated: $(date)"
        echo "==============================================="
        echo ""
        
        echo "Application Status:"
        if curl -s "${APP_URL}/health" | grep -q "healthy"; then
            echo "✓ Application is healthy"
        else
            echo "✗ Application is unhealthy"
        fi
        echo ""
        
        echo "Metrics Summary:"
        curl -s "${APP_URL}/api/v1/metrics" | python3 -m json.tool 2>/dev/null || echo "Metrics unavailable"
        echo ""
        
        echo "Container Status:"
        docker ps --filter "name=25RP19452" --format "table {{.Names}}\t{{.Status}}" || echo "Docker not available"
        echo ""
        
        echo "Report generated at: $(date)"
    } | tee "$report_file"
    
    log_success "Report saved to ${report_file}"
}

# Main execution
main() {
    log_info "Starting health check for ${PROJECT_ID}"
    
    check_app_health
    echo ""
    collect_metrics
    echo ""
    check_containers
    echo ""
    check_k8s_pods
    echo ""
    check_logs
    echo ""
    generate_report
    
    log_success "Health check completed"
}

# Run main function
main
