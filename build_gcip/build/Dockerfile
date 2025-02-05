#######################################
# Stage 1 
FROM ghcr.io/netcracker/base-images-module-base:main as build

USER root

COPY build_gcip/build/pip.conf /etc/pip.conf
COPY build_gcip/build/requirements.txt /build/requirements.txt
COPY build_gcip/scripts /module/scripts
COPY build_gcip/pipegene_plugins /module/scripts/pipegene_plugins
COPY python /python
COPY schemas /module/schemas
COPY python/integration /python/integration

RUN apk update \
    && apk add --no-cache \
        git \
        gcc \
        musl-dev \
        libffi-dev \
        curl \
        bash \
    && curl -fsSL https://github.com/cli/cli/releases/download/v2.41.0/gh_2.41.0_linux_amd64.tar.gz -o gh.tar.gz \
    && tar -xvf gh.tar.gz \
    && mv gh_2.41.0_linux_amd64/bin/gh /usr/local/bin/gh \
    && chmod +x /usr/local/bin/gh \
    && rm -rf gh_2.41.0_linux_amd64 gh.tar.gz \
    && test -d /module/venv || python3 -m venv /module/venv \
    && source /module/venv/bin/activate \
    && pip install --no-deps --no-cache-dir -r /build/requirements.txt \
    && python3 -m pip install /python/integration \
    && python3 -m pip install /python/jschon-sort \
    && python3 -m pip install /python/envgene

#######################################
# Stage 2
FROM ghcr.io/netcracker/base-images-module-base:main

COPY --from=build /module /module

ENV PATH=/module/venv/bin:$PATH

USER ci:ci