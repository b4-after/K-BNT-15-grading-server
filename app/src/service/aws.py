from typing import Optional

from boto3 import client
from pydantic import HttpUrl

from src.constant import AWSS3ClientMethod, AWSServiceName
from src.core import get_settings


class AWSS3Service:
    _AWS_ACCESS_KEY_ID: str = get_settings().AWS_ACCESS_KEY_ID
    _AWS_SECRET_ACCESS_KEY: str = get_settings().AWS_SECRET_ACCESS_KEY
    _AWS_REGION: str = get_settings().AWS_REGION
    _AWS_ENDPOINT_URL: Optional[str] = get_settings().AWS_ENDPOINT_URL

    def __init__(self) -> None:
        self.client: client = client(
            service_name=AWSServiceName.S3.value,
            # endpoint_url=AWSS3Service._AWS_ENDPOINT_URL,
            # aws_access_key_id=AWSS3Service._AWS_ACCESS_KEY_ID,
            # aws_secret_access_key=AWSS3Service._AWS_SECRET_ACCESS_KEY,
            # region_name=AWSS3Service._AWS_REGION,
            # verify=False,
            # use_ssl=False,
        )

    def get_presigned_url(self, object_key: str, bucket_name: str) -> HttpUrl:
        return self.client.generate_presigned_url(
            ClientMethod=AWSS3ClientMethod.GET_OBJECT.value,
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=300,
        )
