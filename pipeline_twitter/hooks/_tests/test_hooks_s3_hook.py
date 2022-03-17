import pytest

from pipeline_twitter.hooks import s3_hook


@pytest.fixture
def boto3_fake(mocker):

    fake = mocker.patch.object(s3_hook, 'boto3')
    return fake.session.Session.return_value.client.return_value


def test_should_get_post_of_twitter(mocker, boto3_fake):

    obj = s3_hook.S3Hook()
    obj.load_string(
        bucket_name='fake-bucket',
        key='fake-file',
        string_data='fake-content',
    )

    boto3_fake.upload_fileobj.assert_called_with(
        mocker.ANY,
        'fake-bucket',
        'fake-file',
    )
