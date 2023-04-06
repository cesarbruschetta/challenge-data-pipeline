import os

from airflow.models import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago


ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
}

with DAG(
    dag_id='transient_to_raw_v1',
    default_args=ARGS,
    schedule_interval='0 10 * * *',
    max_active_runs=1,
) as dag:

    start = DummyOperator(task_id='start')

    save_transient_raw = SparkSubmitOperator(
		application='/app/pipeline_twitter/etls/save_in_raw.py',
		conn_id='spark_default', 
		task_id='run_save_transient_raw',
        conf={
            "spark.kubernetes.container.image":"cesarbruschetta/challenget-data-pipeline:lastest",
            "spark.kubernetes.namespace":"spark-runner",
            "spark.kubernetes.authenticate.driver.serviceAccountName":"spark-runner-service-account",
            "spark.kubernetes.file.upload.path":"/tmp",
            "spark.ui.enabled":"false",
            "spark.kubernetes.driverEnv.MINIO_ENDPOINT": os.getenv("MINIO_ENDPOINT"),
            "spark.kubernetes.driverEnv.MINIO_ACCESS_KEY": os.getenv("MINIO_ACCESS_KEY"),
            "spark.kubernetes.driverEnv.MINIO_SECRET_KEY": os.getenv("MINIO_SECRET_KEY"),
        }
    )

    end = DummyOperator(task_id='end')

    start >> save_transient_raw >> end
