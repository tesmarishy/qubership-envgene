#-----------Stage 1-----------
FROM alpine:3.19 AS initial
WORKDIR /workspace
COPY github_workflows/env_instance_builder/.github /opt/github

#-----------Stage 2-----------
FROM scratch
COPY --from=builder /opt/github /opt/github