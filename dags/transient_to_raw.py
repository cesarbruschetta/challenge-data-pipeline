import os

from airflow.models import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago


ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(6),
}

with DAG(
    dag_id='transient_to_raw_v1',
    default_args=ARGS,
    schedule_interval='0 10 * * *',
    max_active_runs=1,
) as dag:

    start = DummyOperator(task_id='start')

    save_transient_raw = KubernetesPodOperator(
        task_id='run_save_transient_raw',
        name='run_save_transient_raw',
        cmds=[
            '/usr/bin/python3.9',
            '/app/pipeline_twitter/etls/save_in_raw.py',
            '--process-date={{ ds }}',
        ],
        image_pull_policy="Always",
        namespace='airflow',
        image="cesarbruschetta/challenget-data-pipeline:lastest",
        is_delete_operator_pod=True,
        env_vars={
            "MINIO_ENDPOINT": os.getenv("MINIO_ENDPOINT"),
            "MINIO_ACCESS_KEY": os.getenv("MINIO_ACCESS_KEY"),
            "MINIO_SECRET_KEY": os.getenv("MINIO_SECRET_KEY"),
        },
    )

    end = DummyOperator(task_id='end')

    start >> save_transient_raw >> end
