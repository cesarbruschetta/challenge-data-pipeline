from pathlib import Path

from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.models import DAG, Variable
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(6),
}
BASE_FOLDER = Path(__file__).parent

with DAG(
    dag_id='transient_to_raw',
    default_args=ARGS,
    schedule_interval='0 10 * * *',
    max_active_runs=1,
) as dag:

    start = DummyOperator(task_id='start')

    save_transient_raw = SparkSubmitOperator(
        task_id="run_save_transient_raw",
        application=f"{BASE_FOLDER}/etls/save_in_raw.py",
        name="twitter_save_transient_raw",
        application_args=[
            "--process-date",
            "{{ ds }}",
        ],
        conn_id="spark_default",
        env_vars={
            "MINIO_ACCESS_KEY": Variable.get("MINIO_ACCESS_KEY", default_var=None),
            "MINIO_SECRET_KEY": Variable.get("MINIO_SECRET_KEY", default_var=None),
        },
        packages=",".join([
            "com.amazonaws:aws-java-sdk-bundle:1.11.819",
            "org.apache.hadoop:hadoop-aws:3.2.0",
        ])
    )

    end = DummyOperator(task_id='end')

    start >> save_transient_raw >> end
