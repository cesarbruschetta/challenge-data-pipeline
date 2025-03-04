from pipeline_twitter.etls.save_in_transient import SaveTwitterInTransientZone


def test_should_save_post_of_twitter_in_tansient_zone(
    mocker, boto3_s3_fake, request_twitter_fake
):

    obj = SaveTwitterInTransientZone(
        query='AluraOnline',
        twitter_token='faketoken',
        start_time='2020-01-01',
        end_time='2020-01-02',
    )
    obj.run()

    boto3_s3_fake.upload_fileobj.assert_called_with(
        mocker.ANY,
        'lake-transient-challenge',
        mocker.ANY,
    )
