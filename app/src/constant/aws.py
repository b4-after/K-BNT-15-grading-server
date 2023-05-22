from enum import Enum


class AWSServiceName(str, Enum):
    S3: str = "s3"
    SQS: str = "sqs"


class AWSS3ClientMethod(str, Enum):
    GET_OBJECT: str = "get_object"
