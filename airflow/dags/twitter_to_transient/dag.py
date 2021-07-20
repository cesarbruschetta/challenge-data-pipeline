from pathlib import Path

from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago


ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(6),
}
BASE_FOLDER = Path(__file__).parent


with DAG(
    dag_id='twitter_to_transient',
    default_args=ARGS,
    schedule_interval='0 9 * * *',
    max_active_runs=1,
) as dag:

    start = DummyOperator(task_id='start')
    save_transient = BashOperator(
        task_id='run_save_transient',
        bash_command=(
            f'python {BASE_FOLDER}/etls/save_in_transient.py '
            '--start_time={{ yesterday_ds }} '
            '--end_time={{ ds }} '
        ),
    )
    end = DummyOperator(task_id='end')

    start >> save_transient >> end
