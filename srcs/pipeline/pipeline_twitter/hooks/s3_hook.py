import io
import os
from io import BytesIO
from typing import Optional

import boto3
from botocore.client import Config


class S3Hook:
    def get_conn(self) -> boto3.Session:
        session = boto3.session.Session()
        return session.client(
            's3',
            endpoint_url=os.getenv("MINIO_ENDPOINT"),
            aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
            config=Config(signature_version='s3v4'),
            region_name='us-east-1',
        )

    def load_string(
        self,
        string_data: str,
        key: str,
        bucket_name: Optional[str] = None,
    ) -> None:

        encoding = 'utf-8'
        bytes_data = string_data.encode(encoding)

        file_obj = io.BytesIO(bytes_data)

        self._upload_file_obj(file_obj, key, bucket_name)
        file_obj.close()

    def _upload_file_obj(
        self,
        file_obj: BytesIO,
        key: str,
        bucket_name: Optional[str] = None,
    ) -> None:

        client = self.get_conn()
        client.upload_fileobj(
            file_obj,
            bucket_name,
            key,
        )
