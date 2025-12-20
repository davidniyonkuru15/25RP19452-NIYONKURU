#!/bin/bash

################################################################################
# DockerHub Push Script - Campus IT Helpdesk Microservice
# Project ID: 25RP19452-NIYONKURU
# Purpose: Push Docker image to DockerHub registry
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Project variables
PROJECT_ID="25RP19452-NIYONKURU"
PROJECT_ID_LOWER="25rp19452-niyonkuru"
IMAGE_NAME="$PROJECT_ID_LOWER/helpdesk"
VERSION="1.0.0"
DOCKER_REGISTRY="docker.io"

echo "================================================"
echo "DockerHub Push - Campus IT Helpdesk"
echo "Project ID: $PROJECT_ID"
echo "================================================"
echo ""

# Function to print messages
print_section() {
    echo -e "${BLUE}[*] $1${NC}"
}

print_success() {
    echo -e "${GREEN}[✓] $1${NC}"
}

print_error() {
    echo -e "${RED}[✗] $1${NC}"
}

# 1. Check if Docker is running
print_section "Checking Docker daemon..."
if ! docker ps > /dev/null 2>&1; then
    print_error "Docker daemon is not running"
    exit 1
fi
print_success "Docker daemon is running"

# 2. Check local image exists
print_section "Checking for local Docker image..."
if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "$IMAGE_NAME:latest"; then
    print_success "Local image found: $IMAGE_NAME:latest"
else
    print_error "Local image not found: $IMAGE_NAME:latest"
    echo "Building image first..."
    docker build -f docker/Dockerfile -t "$IMAGE_NAME:latest" -t "$IMAGE_NAME:$VERSION" .
    print_success "Image built successfully"
fi

# 3. Check DockerHub credentials
print_section "Checking DockerHub credentials..."
if [ -z "$DOCKERHUB_USERNAME" ] && [ -z "$DOCKERHUB_TOKEN" ]; then
    print_error "DockerHub credentials not found"
    echo ""
    echo "Please set the following environment variables:"
    echo "  export DOCKERHUB_USERNAME=<your-dockerhub-username>"
    echo "  export DOCKERHUB_TOKEN=<your-dockerhub-token>"
    echo ""
    echo "Or log in with: docker login"
    exit 1
fi

if [ -n "$DOCKERHUB_USERNAME" ] && [ -n "$DOCKERHUB_TOKEN" ]; then
    print_section "Logging into DockerHub..."
    echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
    print_success "Logged into DockerHub as $DOCKERHUB_USERNAME"
fi

# 4. Tag image for DockerHub
print_section "Tagging image for DockerHub..."
docker tag "$IMAGE_NAME:latest" "$DOCKER_REGISTRY/$IMAGE_NAME:latest"
docker tag "$IMAGE_NAME:latest" "$DOCKER_REGISTRY/$IMAGE_NAME:$VERSION"
docker tag "$IMAGE_NAME:latest" "$DOCKER_REGISTRY/$IMAGE_NAME:$(date +%Y%m%d-%H%M%S)"
print_success "Image tagged successfully"

# 5. Push to DockerHub
print_section "Pushing to DockerHub..."
echo ""
echo "🐳 Pushing: $DOCKER_REGISTRY/$IMAGE_NAME:latest"
docker push "$DOCKER_REGISTRY/$IMAGE_NAME:latest"

echo ""
echo "🐳 Pushing: $DOCKER_REGISTRY/$IMAGE_NAME:$VERSION"
docker push "$DOCKER_REGISTRY/$IMAGE_NAME:$VERSION"

# 6. Display results
echo ""
print_success "Image pushed to DockerHub successfully!"
echo ""
echo "📦 Image locations:"
echo "   • $DOCKER_REGISTRY/$IMAGE_NAME:latest"
echo "   • $DOCKER_REGISTRY/$IMAGE_NAME:$VERSION"
echo ""
echo "✅ To pull this image, use:"
echo "   docker pull $DOCKER_REGISTRY/$IMAGE_NAME:latest"
echo "   docker pull $DOCKER_REGISTRY/$IMAGE_NAME:$VERSION"
echo ""
echo "View on DockerHub: https://hub.docker.com/r/$IMAGE_NAME"
echo ""

print_success "DockerHub push completed!"
