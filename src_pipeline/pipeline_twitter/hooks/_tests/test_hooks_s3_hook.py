from pipeline_twitter.hooks.s3_hook import S3Hook


def test_should_save_file_in_s3(mocker, boto3_s3_fake):

    obj = S3Hook()
    obj.load_string(
        bucket_name='fake-bucket',
        key='fake-file',
        string_data='fake-content',
    )

    boto3_s3_fake.upload_fileobj.assert_called_with(
        mocker.ANY,
        'fake-bucket',
        'fake-file',
    )
