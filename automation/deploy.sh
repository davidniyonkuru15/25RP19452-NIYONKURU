#!/bin/bash

#############################################################################
# Campus IT Helpdesk - Infrastructure Deployment Script
# Student ID: 25RP19452-NIYONKURU
# Purpose: Automated infrastructure setup for development environment
#############################################################################

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
REPO_URL="https://github.com/your-org/25RP19452-NIYONKURU-helpdesk.git"
BRANCH="main"
WORKSPACE_DIR="/home/vboxuser/25RP19452_NIYONKURU_IT_HELP_DESK"
LOG_FILE="${WORKSPACE_DIR}/deployment.log"

# Initialize logging
mkdir -p "${WORKSPACE_DIR}/logs"
exec 1> >(tee -a "${LOG_FILE}")
exec 2>&1

log_info "========================================"
log_info "Campus IT Helpdesk - Infrastructure Setup"
log_info "Project ID: ${PROJECT_ID}"
log_info "========================================"

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local required_tools=("docker" "docker-compose" "kubectl" "git" "python3" "pip3")
    
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "$tool is not installed"
            exit 1
        fi
    done
    
    log_success "All prerequisites are installed"
}

# Initialize directory structure
init_directories() {
    log_info "Initializing directory structure..."
    
    mkdir -p "${WORKSPACE_DIR}/25RP19452-NIYONKURU"/{src,tests,docker,kubernetes,ci-cd,monitoring,automation,docs/evidence}
    mkdir -p "${WORKSPACE_DIR}/logs"
    mkdir -p "${WORKSPACE_DIR}/backups"
    
    log_success "Directory structure initialized"
}

# Initialize Git repository
init_git() {
    log_info "Initializing Git repository..."
    
    cd "${WORKSPACE_DIR}/25RP19452-NIYONKURU"
    
    if [ ! -d ".git" ]; then
        git init
        git config user.email "devops@university.edu"
        git config user.name "DevOps Engineer - 25RP19452-NIYONKURU"
        git branch -M main
        log_success "Git repository initialized"
    else
        log_warning "Git repository already exists"
    fi
}

# Build Docker image
build_docker_image() {
    log_info "Building Docker image..."
    
    cd "${WORKSPACE_DIR}/25RP19452-NIYONKURU"
    
    docker build -f docker/Dockerfile \
        -t "25rp19452-niyonkuru/helpdesk:1.0.0" \
        -t "25rp19452-niyonkuru/helpdesk:latest" \
        .
    
    log_success "Docker image built successfully"
    docker images | grep 25rp19452-niyonkuru
}

# Run tests
run_tests() {
    log_info "Running unit tests..."
    
    cd "${WORKSPACE_DIR}/25RP19452-NIYONKURU"
    
    pip3 install -q -r requirements.txt
    python3 -m pytest tests/ -v --tb=short
    
    log_success "Tests completed"
}

# Start Docker containers
start_containers() {
    log_info "Starting Docker containers..."
    
    cd "${WORKSPACE_DIR}/25RP19452-NIYONKURU"
    
    docker-compose up -d
    
    sleep 5
    
    if docker ps | grep -q "25RP19452-NIYONKURU-helpdesk"; then
        log_success "Containers started successfully"
        docker ps --filter "label=com.docker.compose.project"
    else
        log_error "Failed to start containers"
        exit 1
    fi
}

# Verify application health
verify_application() {
    log_info "Verifying application health..."
    
    sleep 3
    
    if curl -s http://localhost:5000/health | grep -q "healthy"; then
        log_success "Application is healthy"
    else
        log_error "Application health check failed"
        exit 1
    fi
}

# Create sample tickets
create_sample_data() {
    log_info "Creating sample tickets..."
    
    curl -s -X POST http://localhost:5000/api/v1/tickets \
        -H "Content-Type: application/json" \
        -d '{
            "title": "Network connectivity issue",
            "description": "Cannot connect to lab computers",
            "category": "network",
            "priority": "high",
            "submitter_email": "student@university.edu",
            "submitter_name": "John Doe"
        }' | tee >> "${LOG_FILE}"
    
    log_success "Sample data created"
}

# Main execution
main() {
    log_info "Starting deployment process..."
    
    check_prerequisites
    init_directories
    init_git
    build_docker_image
    run_tests
    start_containers
    verify_application
    create_sample_data
    
    log_success "========================================"
    log_success "Infrastructure setup completed successfully!"
    log_success "========================================"
    log_success "Application URL: http://localhost:5000"
    log_success "API Documentation: http://localhost:5000/api/v1"
    log_success "Health Check: http://localhost:5000/health"
}

# Run main function
main
