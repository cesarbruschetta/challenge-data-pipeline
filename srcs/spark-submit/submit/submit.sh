#!/bin/bash

# Path to ServiceAccount token
SERVICE_ACCOUNT_PATH=/var/run/secrets/kubernetes.io/serviceaccount
NAMESPACE=$(cat ${SERVICE_ACCOUNT_PATH}/namespace)
TOKEN=${SERVICE_ACCOUNT_PATH}/token
CA_CERT=${SERVICE_ACCOUNT_PATH}/ca.crt


$SPARK_HOME/bin/spark-submit \
  --master=k8s://https://kubernetes.default.svc \
  --deploy-mode=cluster \
  --name=$APP_NAME \
  --driver-java-options="-Dlog4j.configuration=file:conf/log4j.properties" \
  --conf spark.ui.enabled=true \
  --conf spark.executor.instances=3 \
  --conf spark.kubernetes.file.upload.path=/tmp \
  --conf spark.kubernetes.namespace=$NAMESPACE \
  --conf spark.kubernetes.container.image=$IMAGE \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=$SERVICE_ACCOUNT \
  --conf spark.kubernetes.authenticate.submission.caCertFile=$CA_CERT \
  --conf spark.kubernetes.authenticate.oauthTokenFile=$TOKEN \
  --conf spark.kubernetes.driverEnv.MINIO_ENDPOINT=$MINIO_ENDPOINT \
  --conf spark.kubernetes.driverEnv.MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY \
  --conf spark.kubernetes.driverEnv.MINIO_SECRET_KEY=$MINIO_SECRET_KEY \
  local://$FILE_PATH

