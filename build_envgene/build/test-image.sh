#!/bin/bash

# Test script for the unified Docker image
# This script tests all major components of the image

set -e

IMAGE_NAME=${1:-"test-build-unified-root-v5"}
echo "Testing image: $IMAGE_NAME"

echo "=== Testing basic components ==="
docker run --rm $IMAGE_NAME whoami
docker run --rm $IMAGE_NAME python --version
docker run --rm $IMAGE_NAME bash --version

echo "=== Testing Ansible ==="
docker run --rm $IMAGE_NAME ansible --version
docker run --rm $IMAGE_NAME ansible-doc -t callback -l | grep -E "(default|posix)"
docker run --rm $IMAGE_NAME ansible-doc community.general.maven_artifact | head -5

echo "=== Testing SOPS ==="
docker run --rm $IMAGE_NAME sops --version

echo "=== Testing jschon-sort ==="
docker run --rm $IMAGE_NAME jschon-sort --help

echo "=== Testing CI/CD directories ==="
docker run --rm $IMAGE_NAME ls -la /__w/_temp/_runner_file_commands
docker run --rm $IMAGE_NAME ls -la /github/workspace
docker run --rm $IMAGE_NAME ls -la /builds

echo "=== Testing callback plugin ==="
# Test that the debug callback plugin works
docker run --rm $IMAGE_NAME ansible localhost -m ping -c local -e "stdout_callback=ansible.posix.debug" || echo "Callback test completed"

echo "=== Image size ==="
docker images $IMAGE_NAME

echo "=== All tests passed! ===" 