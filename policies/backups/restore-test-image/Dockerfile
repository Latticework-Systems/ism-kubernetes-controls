# kubectl v1.36.2; this image is intentionally amd64 because the downloaded
# Velero and jq binaries below are amd64 artifacts.
FROM --platform=linux/amd64 docker.io/bitnami/kubectl@sha256:4eb84ef6cad87ff410066c0d94bf7f10ccf298b0d5efa4f194e37c8a3b0aa182

USER root

ARG VELERO_VERSION=v1.13.0
ARG VELERO_SHA256=4cbb18a05c0dd3e60430e015e90d53fddbf4111a0252ea27877a8cea42bdea8f
ARG JQ_VERSION=jq-1.7.1
ARG JQ_SHA256=5942c9b0934e510ee61eb3e30273f1b3fe2590df93933a93d7c58b81d19c8ff5

RUN install_packages curl tar && \
    curl -fsSL "https://github.com/vmware-tanzu/velero/releases/download/${VELERO_VERSION}/velero-${VELERO_VERSION}-linux-amd64.tar.gz" \
      -o /tmp/velero.tar.gz && \
    echo "${VELERO_SHA256}  /tmp/velero.tar.gz" | sha256sum -c - && \
    tar xzf /tmp/velero.tar.gz -C /tmp && \
    install -m 0755 "/tmp/velero-${VELERO_VERSION}-linux-amd64/velero" /usr/local/bin/velero && \
    curl -fsSL "https://github.com/jqlang/jq/releases/download/${JQ_VERSION}/jq-linux-amd64" \
      -o /tmp/jq && \
    echo "${JQ_SHA256}  /tmp/jq" | sha256sum -c - && \
    install -m 0755 /tmp/jq /usr/local/bin/jq && \
    rm -rf /tmp/velero-* /tmp/velero.tar.gz /tmp/jq

USER 1001
