#!/bin/bash

#############################################################################
# Campus IT Helpdesk - Kubernetes Deployment Script
# Student ID: 25RP19452-NIYONKURU
# Purpose: Deploy microservice to Kubernetes cluster
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

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration
PROJECT_ID="25RP19452-NIYONKURU"
NAMESPACE="25rp19452-niyonkuru"
KUBE_CONFIG="${HOME}/.kube/config"
WORKSPACE_DIR="/home/vboxuser/25RP19452_NIYONKURU_IT_HELP_DESK/25RP19452-NIYONKURU"

log_info "Kubernetes Deployment Script for ${PROJECT_ID}"

# Check prerequisites
check_k8s_prerequisites() {
    log_info "Checking Kubernetes prerequisites..."
    
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed"
        exit 1
    fi
    
    if [ ! -f "$KUBE_CONFIG" ]; then
        log_error "Kubernetes configuration not found"
        exit 1
    fi
    
    log_success "Kubernetes prerequisites verified"
}

# Create namespace
create_namespace() {
    log_info "Creating namespace: ${NAMESPACE}"
    
    kubectl apply -f "${WORKSPACE_DIR}/kubernetes/namespace.yaml"
    
    log_success "Namespace created"
}

# Create storage
create_storage() {
    log_info "Creating persistent volumes and claims..."
    
    kubectl apply -f "${WORKSPACE_DIR}/kubernetes/storage.yaml"
    
    log_success "Storage resources created"
}

# Deploy RBAC
deploy_rbac() {
    log_info "Deploying RBAC..."
    
    kubectl apply -f "${WORKSPACE_DIR}/kubernetes/rbac.yaml"
    
    log_success "RBAC deployed"
}

# Deploy ConfigMap
deploy_configmap() {
    log_info "Deploying ConfigMap..."
    
    kubectl apply -f "${WORKSPACE_DIR}/kubernetes/configmap.yaml"
    
    log_success "ConfigMap deployed"
}

# Deploy application
deploy_application() {
    log_info "Deploying application..."
    
    kubectl apply -f "${WORKSPACE_DIR}/kubernetes/deployment.yaml"
    
    log_success "Deployment created"
}

# Deploy service
deploy_service() {
    log_info "Deploying service..."
    
    kubectl apply -f "${WORKSPACE_DIR}/kubernetes/service.yaml"
    
    log_success "Service deployed"
}

# Deploy HPA
deploy_hpa() {
    log_info "Deploying Horizontal Pod Autoscaler..."
    
    kubectl apply -f "${WORKSPACE_DIR}/kubernetes/hpa.yaml"
    
    log_success "HPA deployed"
}

# Deploy monitoring
deploy_monitoring() {
    log_info "Deploying monitoring stack..."
    
    kubectl apply -f "${WORKSPACE_DIR}/monitoring/prometheus.yaml"
    kubectl apply -f "${WORKSPACE_DIR}/monitoring/grafana.yaml"
    kubectl apply -f "${WORKSPACE_DIR}/monitoring/loki.yaml"
    
    log_success "Monitoring stack deployed"
}

# Wait for rollout
wait_for_rollout() {
    log_info "Waiting for application rollout..."
    
    kubectl rollout status deployment/helpdesk-app -n "${NAMESPACE}" --timeout=5m
    
    log_success "Rollout completed"
}

# Get service endpoint
get_endpoints() {
    log_info "Service endpoints:"
    
    echo ""
    echo "Main Application:"
    kubectl get service helpdesk-service -n "${NAMESPACE}"
    
    echo ""
    echo "Pods:"
    kubectl get pods -n "${NAMESPACE}"
    
    echo ""
    echo "Access application at:"
    kubectl get service helpdesk-service -n "${NAMESPACE}" -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
}

# Main execution
main() {
    log_info "Starting Kubernetes deployment..."
    
    check_k8s_prerequisites
    create_namespace
    create_storage
    deploy_rbac
    deploy_configmap
    deploy_application
    deploy_service
    deploy_hpa
    deploy_monitoring
    wait_for_rollout
    
    log_success "========================================"
    log_success "Kubernetes deployment completed!"
    log_success "========================================"
    
    get_endpoints
}

main
