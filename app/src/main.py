import json
from logging import DEBUG, Logger, getLogger

from src.constant import HTTPStatusCode
from src.custom import (
    AWSS3,
    AWSLambdaContext,
    AWSLambdaEventBody,
    AWSS3Event,
    HTTPResponse,
    NotFoundError,
)
from src.service import AnswerService


def lambda_handler(event: AWSLambdaEventBody, context: AWSLambdaContext) -> HTTPResponse:
    import os
    import subprocess

    javac_location = subprocess.check_output(["which", "javac"]).strip().decode()
    real_path = os.path.realpath(javac_location)
    java_home = os.path.dirname(os.path.dirname(real_path))
    print(java_home)
    os.environ["JAVA_HOME"] = java_home

    logger: Logger = getLogger()
    logger.setLevel(level=DEBUG)
    answer: AnswerService = AnswerService()
    try:
        s3_event: AWSS3Event = json.loads(s=event.get("Records").pop().get("body"))
        s3_information: AWSS3 = s3_event.get("Records").pop().get("s3")
        answer.grade(s3_information=s3_information)
        return HTTPResponse(
            statusCode=HTTPStatusCode.OK.value,
            headers={"Content-Type": "application/json"},
            body=json.dumps({"detail": "Success"}),
        )

    except NotFoundError as not_found_error:
        return HTTPResponse(
            statusCode=HTTPStatusCode.NOT_FOUND.value,
            headers={"Content-Type": "application/json"},
            body=json.dumps({"detail": str(not_found_error)}),
        )

    except ValueError as value_error:
        return HTTPResponse(
            statusCode=HTTPStatusCode.UNPROCESSABLE_ENTITY.value,
            headers={"Content-Type": "application/json"},
            body=json.dumps({"detail": str(value_error)}),
        )

    except Exception as error:
        return HTTPResponse(
            statusCode=HTTPStatusCode.INTERNAL_SERVER_ERROR.value,
            headers={"Content-Type": "application/json"},
            body=json.dumps({"detail": str(error)}),
        )
