FROM registry.access.redhat.com/ubi9/ubi-micro

ARG JAVA_PACKAGE=java-17-openjdk-headless
ARG RUN_JAVA_VERSION=1.3.8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en'

RUN microdnf install -y curl ca-certificates ${JAVA_PACKAGE} && \
    microdnf clean all && \
    mkdir -p /deployments && \
    chown 1001:root /deployments && \
    chmod g+rwX /deployments && \
    curl -s https://repo1.maven.org/maven2/io/fabric8/run-java-sh/${RUN_JAVA_VERSION}/run-java-sh-${RUN_JAVA_VERSION}-sh.sh -o /deployments/run-java.sh && \
    chmod 540 /deployments/run-java.sh && \
    echo "securerandom.source=file:/dev/urandom" >> /etc/alternatives/jre/lib/security/java.security

COPY --chown=1001:root downloaded_artifact/build_effective_set_generator_java/effective-set-generator/target/*.jar /deployments/app.jar

USER 1001

ENTRYPOINT [ "/deployments/run-java.sh" ]