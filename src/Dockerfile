FROM apache/spark-py:v3.3.0

ENV PYTHONPATH=/app
ENV HADOOP_VERSION=3.3.0
ENV AWS_SDK_VERSION=1.12.310

ENV SCALA_VERSION=2.12.15
ENV JAVA_VERSION=11.0.15

USER root

# The below jars are needed so Hadoop can use aws.
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget && \
    wget "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar" -P /opt/spark/jars/ && \
    wget "https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar" -P /opt/spark/jars/ && \
    wget "https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/${AWS_SDK_VERSION}/aws-java-sdk-${AWS_SDK_VERSION}.jar" -P /opt/spark/jars/ && \
    wget "https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-core/${AWS_SDK_VERSION}/aws-java-sdk-core-${AWS_SDK_VERSION}.jar" -P /opt/spark/jars/ && \
    wget "https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-s3/${AWS_SDK_VERSION}/aws-java-sdk-s3-${AWS_SDK_VERSION}.jar" -P /opt/spark/jars/ && \
    wget "https://repo1.maven.org/maven2/com/google/guava/guava/31.1-jre/guava-31.1-jre.jar" -P /opt/spark/jars/ && \
    # Remove duplicated class
    rm -f /hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.30.jar && \
    rm -f /opt/spark/jars/guava-14.0.1.jar && \
    rm -rf /var/lib/apt/lists/*

# copy the code
ADD ./pipeline_twitter /app/pipeline_twitter
ADD ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN python3 -m pip install -r /app/requirements.txt

# Set the working directory
WORKDIR /app
