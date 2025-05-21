FROM registry.access.redhat.com/ubi9/openjdk-17 as builder
WORKDIR /work
COPY downloaded_artifact/build_effective_set_generator_java/effective-set-generator/target/effective-set-generator-master-SNAPSHOT-runner.jar app.jar

RUN jdeps --print-module-deps --ignore-missing-deps app.jar > mods && \
    jlink --add-modules $(cat mods) \
          --strip-debug --compress=2 \
          --output jre

FROM registry.access.redhat.com/ubi9/ubi-micro
COPY --from=builder /work/jre /opt/jre
COPY --from=builder /work/app.jar /app.jar
USER 1001
ENV PATH="/opt/jre/bin:${PATH}"
ENTRYPOINT ["java","-jar","/app.jar"]