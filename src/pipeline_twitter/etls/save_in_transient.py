import argparse
import json
import os
import uuid
from datetime import datetime

from pipeline_twitter.hooks.s3_hook import S3Hook
from pipeline_twitter.hooks.twitter_hook import TwitterHook


class SaveTwitterInTransientZone:
    def __init__(
        self,
        query: str,
        twitter_token: str,
        start_time: str,
        end_time: str,
    ) -> None:

        self.start_time = datetime.strptime(start_time, '%Y-%m-%d')
        self.end_time = datetime.strptime(end_time, '%Y-%m-%d')

        self.twitter = TwitterHook(
            query=query,
            token=twitter_token,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        # Save file in Storage
        self.storage = S3Hook()

    def run(self) -> None:
        for twitter_pg in self.twitter.run():
            page = uuid.uuid4()
            self.storage.load_string(
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
        twitter_token=os.getenv('TWITTER_BEARER_TOKEN', ''),
        start_time=args.start_time,
        end_time=args.end_time,
    )
    obj.run()
