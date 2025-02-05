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
    && test -d /module/venv || python3 -m venv /module/venv \
    && source /module/venv/bin/activate \
    && pip install --no-deps --no-cache-dir -r /build/requirements.txt \
    && python3 -m pip install /python/integration \
    && python3 -m pip install /python/jschon-sort \
    && python3 -m pip install /python/envgene

#######################################
# Stage 2
FROM ghcr.io/netcracker/base-images-module-base:main

USER root

COPY --from=build /module /module

RUN apk update \
    && apk add --no-cache \
        git \
        curl \
    && echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
    && apk add --no-cache github-cli@community \
    && git config --global --add safe.directory /repo

ENV PATH=/module/venv/bin:/usr/bin:/usr/local/bin:$PATH

USER ci:ci