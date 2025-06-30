#########################################
## Stage 1: Builder
FROM python:3.11-slim as builder

USER root

# Copy only files needed for installation first to leverage Docker cache
COPY build_envgene/build/pip.conf /etc/pip.conf
COPY build_envgene/build/requirements.txt /build/requirements.txt
COPY build_envgene/build/requirements.yml /build/requirements.yml

# Install build dependencies and runtime packages in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        python3-cryptography \
        python3-openssl \
        openssh-client \
        ca-certificates \
        coreutils \
        curl \
        sudo \
        zip \
        unzip \
        jq \
        # Build dependencies
        build-essential \
        libxml2-dev \
        libxslt-dev \
        zlib1g-dev && \
    # Install sops
    curl --retry 3 --retry-connrefused --retry-delay 5 -LO https://github.com/mozilla/sops/releases/download/v3.9.0/sops-v3.9.0.linux.amd64 && \
    chmod +x sops-v3.9.0.linux.amd64 && \
    mv sops-v3.9.0.linux.amd64 /usr/local/bin/sops && \
    # Install Python packages
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /build/requirements.txt && \
    mkdir -p /module/ansible/collections && \
    ansible-galaxy collection install -r /build/requirements.yml -p /module/ansible/collections && \
    pip install --no-cache-dir PyYAML && \
    # Cleanup
    apt-get remove -y build-essential libxml2-dev libxslt-dev zlib1g-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache

# Copy remaining application files
COPY build_envgene/ansible /module/ansible
COPY build_envgene/scripts /module/scripts
COPY build_envgene/workflows /workflows
COPY python /python

COPY build_* create_* produce_* sort* /build_env/
COPY scripts /build_env/scripts
COPY env-builder /build_env/env-builder
COPY schemas /build_env/schemas

# Install local Python packages
RUN pip install --no-cache-dir \
    /python/jschon-sort \
    /python/envgene \
    /python/integration && \
    chmod 754 /module/scripts/* && \
    # Cleanup pip cache
    rm -rf /root/.cache

ENV ANSIBLE_LIBRARY=/module/ansible/library

WORKDIR /module/ansible
