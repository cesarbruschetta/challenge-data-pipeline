import pytest

from pipeline_twitter.hooks import s3_hook, twitter_hook


@pytest.fixture
def request_twitter_fake(mocker):

    data = {
        'data': [
            {
                'public_metrics': {
                    'retweet_count': 0,
                    'reply_count': 0,
                    'like_count': 0,
                    'quote_count': 0,
                },
                'id': '1503353353903951876',
                'in_reply_to_user_id': '1566580880',
                'text': '@AluraOnline ah eu terminei 19',
                'created_at': '2022-03-14T12:52:25.000Z',
                'conversation_id': '1274600262930501632',
                'author_id': '255124931',
            },
            {
                'public_metrics': {
                    'retweet_count': 0,
                    'reply_count': 0,
                    'like_count': 0,
                    'quote_count': 0,
                },
                'id': '1503347656164270081',
                'in_reply_to_user_id': '1566580880',
                'text': '@AluraOnline Ahhhh 💓💓💓💓💓💓💓💓',
                'created_at': '2022-03-14T12:29:46.000Z',
                'conversation_id': '1274600262930501632',
                'author_id': '255124931',
            },
        ],
        'includes': {
            'users': [
                {
                    'id': '1274600262930501632',
                    'name': 'gabrielle with an e',
                    'username': 'gab_inh4',
                    'created_at': '2020-06-21T07:09:33.000Z',
                },
                {
                    'id': '255124931',
                    'name': 'Emilyn!🕉️☯️☮️✨✨🎮🕹️🖥️',
                    'username': 'YeLimn_',
                    'created_at': '2011-02-20T18:40:57.000Z',
                },
            ]
        },
        'meta': {
            'newest_id': '1503353353903951876',
            'oldest_id': '1503186578654613507',
            'result_count': 10,
            'next_token': 'b26v89c19zqg8o3fpyqmi59jjxzszfhaz32iqz0rotlrx',
        },
    }
    data2 = data.copy()
    data2['meta'] = {}

    fake = mocker.patch.object(twitter_hook, 'requests')
    fake.get.return_value.json.side_effect = (
        data, data2

    )
    return fake


@pytest.fixture
def boto3_s3_fake(mocker):

    fake = mocker.patch.object(s3_hook, 'boto3')
    return fake.session.Session.return_value.client.return_value
