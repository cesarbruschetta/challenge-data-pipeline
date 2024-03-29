import os

from airflow.models import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago


ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(5),
}

with DAG(
    dag_id='twitter_to_transient_v1',
    default_args=ARGS,
    schedule_interval='0 9 * * *',
    max_active_runs=1,
) as dag:

    start = DummyOperator(task_id='start')
    save_transient =  KubernetesPodOperator(
        task_id='run_save_transient',
        name='run_save_transient',
        cmds=[
            '/usr/bin/python3.9',
            '/app/pipeline_twitter/etls/save_in_transient.py',
            '--start_time={{ yesterday_ds }}',
            '--end_time={{ ds }}',
        ],
        image_pull_policy="Always",
        namespace='airflow',
        image="localhost:5001/challenget-data-pipeline:lastest",
        is_delete_operator_pod=True,
        env_vars={
            "TWITTER_BEARER_TOKEN": os.getenv("TWITTER_BEARER_TOKEN"),
            "MINIO_ENDPOINT": os.getenv("MINIO_ENDPOINT"),
            "MINIO_ACCESS_KEY": os.getenv("MINIO_ACCESS_KEY"),
            "MINIO_SECRET_KEY": os.getenv("MINIO_SECRET_KEY"),
        },
    )
    end = DummyOperator(task_id='end')

    start >> save_transient >> end
