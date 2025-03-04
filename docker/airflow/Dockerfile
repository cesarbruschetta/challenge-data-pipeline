FROM apache/airflow:2.1.2

ARG openjdk_version="11"

USER root

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    "openjdk-${openjdk_version}-jre-headless" \
    ca-certificates-java && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${AIRFLOW_UID}

COPY ./requirements.txt /
RUN python3 -m pip install -r /requirements.txt
