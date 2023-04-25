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

    process = subprocess.Popen(
        f'/bin/bash -c {BASE_PATH}/submit.sh',
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True,
        cwd=BASE_PATH,
        env=dict(os.environ, **{
            'APP_NAME': app_name,
            'IMAGE': image,
            'SERVICE_ACCOUNT': service_account,
            'FILE_PATH': file_path,
        })
    )
    stdout, stderr = process.communicate()
    if process.returncode !=0:
        logger.error(f'Failed to run spark-submit. stderr={stderr}')
        raise SystemExit(f'Failed to run spark-submit. stderr={stderr}', code=process.returncode)

    logger.info(f'Finished spark-submit. stdout={stdout}')


if __name__ == "__main__":
    main()
