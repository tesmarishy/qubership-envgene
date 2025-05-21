FROM registry.access.redhat.com/ubi9/openjdk-17 as builder
ARG RUN_JAVA_VERSION=1.3.8
USER 0
WORKDIR /work
COPY downloaded_artifact/build_effective_set_generator_java/effective-set-generator/target/*.jar .

RUN jdeps --print-module-deps --ignore-missing-deps *.jar > /mods && \
    jlink --add-modules $(cat /mods) --strip-debug --compress=2 --output /opt/jre

FROM registry.access.redhat.com/ubi9/ubi-micro
COPY --from=builder /opt/jre /opt/jre
COPY --from=builder /work/*.jar /*.jar
USER 1001
ENV PATH="/opt/jre/bin:${PATH}"
ENTRYPOINT ["java","-jar","/*.jar"]