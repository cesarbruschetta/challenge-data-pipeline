FROM bitnami/spark:3

ARG MAVEN_REPO="https://repo1.maven.org/maven2"
ARG SPARK_JARS_PATH="/opt/bitnami/spark/jars"

RUN curl ${MAVEN_REPO}/com/amazonaws/aws-java-sdk-bundle/1.11.819/aws-java-sdk-bundle-1.11.819.jar \
        --output ${SPARK_JARS_PATH}/aws-java-sdk-bundle-1.11.819.jar \
    && curl ${MAVEN_REPO}/org/apache/hadoop/hadoop-aws/3.2.0/hadoop-aws-3.2.0.jar \
        --output ${SPARK_JARS_PATH}/hadoop-aws-3.2.0.jar
