import types
from datetime import datetime

from pipeline_twitter.hooks.twitter_hook import TwitterHook


def test_should_get_post_of_twitter(mocker, request_twitter_fake):

    obj = TwitterHook(
        token='faketoken',
        query='AluraOnline',
        start_time=datetime(2020, 10, 10),
        end_time=datetime(2020, 11, 11),
    )
    result = obj.run()
    assert isinstance(result, types.GeneratorType) is True

    data = next(result)
    assert 'data' in data.keys()
    assert 'includes' in data.keys()
    assert 'meta' in data.keys()

    next(result)
