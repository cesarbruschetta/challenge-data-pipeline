import argparse
import json
import uuid
from datetime import datetime
from typing import Optional

from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from hooks.twitter_hook import TwitterHook


class SaveTwitterInTransientZone:
    def __init__(
        self,
        query: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> None:

        self.start_time = datetime.strptime(start_time, '%Y-%m-%d')
        self.end_time = datetime.strptime(end_time, '%Y-%m-%d')

        self.twitter = TwitterHook(
            query=query,
            conn_id='twitter_default',
            start_time=self.start_time,
            end_time=self.end_time,
        )

        # Save file in Minio
        self.minio = S3Hook('minio_default')

    def run(self) -> None:
        for twitter_pg in self.twitter.run():
            page = uuid.uuid4()
            self.minio.load_string(
                json.dumps(twitter_pg),
                key=(
                    f'alura_twitters/twitters-{page}-'
                    f'{self.start_time.isoformat()}-'
                    f'{self.end_time.isoformat()}.json'
                ),
                bucket_name='lake-transient-challenge',
            )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SaveTwitterInTransientZone')
    parser.add_argument('--start_time')
    parser.add_argument('--end_time')

    args = parser.parse_args()
    obj = SaveTwitterInTransientZone(
        query='AluraOnline',
        start_time=args.start_time,
        end_time=args.end_time,
    )
    obj.run()
