from datetime import datetime
from typing import Any, Dict, Generator, Optional

from airflow.providers.http.hooks.http import HttpHook


TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.00Z'


class TwitterHook(HttpHook):  # type: ignore
    def __init__(
        self,
        query: str,
        conn_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> None:

        self.query = query
        self.conn_id = conn_id or 'twitter_default'
        self.start_time = start_time
        self.end_time = end_time
        super().__init__(method='GET', http_conn_id=self.conn_id)

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
            f'/2/tweets/search/recent?'
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

    def paginate(
        self, url: str, next_token: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        if next_token is None:
            full_url = url
        else:
            full_url = f'{url}&next_token={next_token}'

        data = super().run(full_url).json()
        yield data

        if 'next_token' in data.get('meta', {}):
            yield from self.paginate(url, data['meta']['next_token'])

    def run(self) -> Generator[Dict[str, Any], None, None]:
        yield from self.paginate(self.create_url())
