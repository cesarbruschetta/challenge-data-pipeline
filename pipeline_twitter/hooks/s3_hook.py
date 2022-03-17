import io
from io import BytesIO
from typing import Optional

import boto3


class S3Hook:
    def get_conn(self) -> boto3.Session:
        session = boto3.session.Session()
        return session.client('s3')

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
