import logging
import subprocess
import os
from pathlib import Path


logging.basicConfig( 
    level=logging.INFO
)
logger = logging.getLogger(__name__)
BASE_PATH = Path(__file__).parent.resolve()

def main():
    logger.info('Starting spark-submit')
    
    app_name = 'transient_to_raw_v1'
    service_account = 'spark-runner-service-account'
    
    image = 'localhost:5001/challenget-data-pipeline:lastest'
    file_path = (
        '/app/pipeline_twitter/etls/save_in_raw.py '
        f'--process-date={os.environ.get("AIRFLOW_PROCESS_DATE")}'
    )

    process = subprocess.run(
        [
            '/bin/bash', "-c",  f'{BASE_PATH}/submit.sh',
        ],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        shell=True,
        check=True,
        cwd=BASE_PATH,
        env=dict(
            os.environ,
            **{
                'APP_NAME': app_name,
                'IMAGE': image,
                'FILE_PATH': file_path,
                'SERVICE_ACCOUNT': service_account,
            }
        )
    )
    process.check_returncode()
    stdout = process.stdout.decode('utf-8')
    logger.info(f'Finished spark-submit. stdout={stdout}')


if __name__ == "__main__":
    main()
