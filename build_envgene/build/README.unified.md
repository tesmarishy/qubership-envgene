# Unified Docker Image for CI/CD

## Overview

This Dockerfile creates a unified, optimized Docker image that combines functionality from both `base_module` and `build_envgene` projects. The image is designed to work seamlessly with both GitHub Actions and GitLab CI environments.

## Key Features

- **Multi-stage build**: Reduces final image size by separating build and runtime stages
- **Alpine Linux base**: Uses `python:3.12-alpine3.19` for a lightweight foundation
- **Root-based execution**: Runs as root to avoid permission issues in CI/CD pipelines
- **CI/CD optimized**: Pre-creates common directories used by GitHub Actions and GitLab CI
- **Minimal dependencies**: Only installs essential packages to reduce attack surface

## Image Size Optimization

The final image size is approximately **343MB**, which is a significant reduction from the original ~1.3GB image. This was achieved through:

1. **Multi-stage build**: Build dependencies are not included in the final image
2. **Alpine Linux**: Much smaller base image compared to Debian/Ubuntu
3. **Aggressive cleanup**: Removes unnecessary files, caches, and test packages
4. **Selective Ansible collections**: Only installs essential collections
5. **Removed build tools**: setuptools and wheel are removed from runtime

## Components Included

- **Python 3.12.8** with virtual environment
- **Ansible Core 2.18.6** with essential collections (ansible.utils, ansible.posix, community.general)
- **SOPS 3.9.0** for secrets management
- **jschon-sort** for JSON Schema sorting
- **envgene** and **integration** Python packages
- **Essential tools**: bash, curl, jq, yq, git, openssh-client, etc.

## CI/CD Compatibility

The image is designed to work with:

### GitHub Actions
- Creates `/__w/_temp/_runner_file_commands` directory
- Creates `/github/workspace` and `/github/home` directories
- Runs as root to avoid permission issues

### GitLab CI
- Creates `/builds` and `/cache` directories
- Compatible with GitLab CI environment variables
- Runs as root for full system access

## Usage

### Building the Image

```bash
docker build -t your-registry/qubership-envgene:latest -f build_envgene/build/Dockerfile.unified .
```

### Running the Container

```bash
# Basic usage
docker run --rm your-registry/qubership-envgene:latest ansible --version

# With volume mounts for CI/CD
docker run --rm -v $(pwd):/workspace your-registry/qubership-envgene:latest ansible-playbook playbook.yml

# Interactive shell
docker run --rm -it your-registry/qubership-envgene:latest bash
```

### GitHub Actions Example

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: your-registry/qubership-envgene:latest
    steps:
      - name: Run Ansible playbook
        run: ansible-playbook playbook.yml
```

### GitLab CI Example

```yaml
build_job:
  image: your-registry/qubership-envgene:latest
  script:
    - ansible-playbook playbook.yml
```

## File Structure

The image contains the following key directories:

- `/module/venv/` - Python virtual environment
- `/module/ansible/` - Ansible configuration and collections
- `/module/scripts/` - Scripts from base_module
- `/build_env/` - Build environment files
- `/python/` - Python package source code
- `/schemas/` - JSON schemas

## Environment Variables

- `PATH=/module/venv/bin:$PATH` - Python virtual environment in PATH
- `PYTHONUNBUFFERED=1` - Unbuffered Python output
- `PYTHONDONTWRITEBYTECODE=1` - Don't write .pyc files
- `ANSIBLE_LIBRARY=/module/ansible/library` - Ansible module path

## Health Check

The image includes a health check that verifies Python is working correctly:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1
```

## Security Considerations

- Runs as root for CI/CD compatibility
- Minimal attack surface with only essential packages
- No unnecessary build tools in runtime
- Regular security updates through Alpine package manager

## Troubleshooting

### Ansible Issues
If Ansible fails to start, ensure that test directories were not accidentally removed during the build process.

**Common Issues:**
- **Callback plugin errors**: If you see "Invalid callback for stdout specified", ensure that the required Ansible collections are installed (ansible.posix for debug callback)
- **Inventory parsing errors**: These are usually related to missing inventory files or permission issues in CI/CD environments

### Permission Issues
The image runs as root, so permission issues should be minimal. If you encounter permission problems, check that the required directories exist and have proper permissions.

### Size Optimization
If you need to further reduce the image size, consider:
- Removing additional Ansible collections
- Using a different base image
- Implementing additional cleanup steps

## Maintenance

- Regularly update the base Alpine image
- Monitor for security updates in Python packages
- Update SOPS to the latest version when available
- Review and update Ansible collections as needed 