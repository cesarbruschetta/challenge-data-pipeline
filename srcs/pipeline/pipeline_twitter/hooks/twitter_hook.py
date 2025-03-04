from datetime import datetime
from typing import Any, Dict, Generator, Optional

import requests
from requests import Response


TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.00Z'


class TwitterHook:
    def __init__(
        self,
        query: str,
        token: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> None:

        self.host = 'api.twitter.com'
        self.query = query
        self.token = token
        self.start_time = start_time
        self.end_time = end_time

    def create_url(self) -> str:
        query = self.query
        tweet_fields = (
            'author_id',
            'conversation_id',
            'created_at',
            'id',
            'in_reply_to_user_id',
            'public_metrics',
            'text',
        )
        expansions = ('author_id',)
        user_fields = ('id', 'name', 'username', 'created_at')
        url = (
            f'https://{self.host}/2/tweets/search/recent?'
            f'query={query}'
            f'&tweet.fields={",".join(tweet_fields)}'
            f'&expansions={",".join(expansions)}'
            f'&user.fields={",".join(user_fields)}'
        )
        if self.start_time:
            url += f'&start_time={self.start_time.strftime(TIMESTAMP_FORMAT)}'
        if self.end_time:
            url += f'&end_time={self.end_time.strftime(TIMESTAMP_FORMAT)}'

        return url

    def request(self, url: str) -> Response:
        resq = requests.get(
            url, headers={'Authorization': f'Bearer {self.token}'}
        )
        resq.raise_for_status()
        return resq

    def paginate(
        self, url: str, next_token: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:

        if next_token is None:
            full_url = url
        else:
            full_url = f'{url}&next_token={next_token}'

        data = self.request(full_url).json()
        yield data

        if 'next_token' in data.get('meta', {}):
            yield from self.paginate(url, data['meta']['next_token'])

    def run(self) -> Generator[Dict[str, Any], None, None]:
        yield from self.paginate(self.create_url())
