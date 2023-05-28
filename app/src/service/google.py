from typing import BinaryIO

from google.cloud.speech import (
    RecognitionAudio,
    RecognitionConfig,
    RecognizeRequest,
    RecognizeResponse,
    SpeechClient,
)
from oauth2client.service_account import ServiceAccountCredentials

from src.constant import GoogleOAuthType, GoogleOAuthURI
from src.core import get_settings


class SpeechToTextService:
    _GOOGLE_CLOUD_PROJECT_ID: str = get_settings().GOOGLE_CLOUD_PROJECT_ID
    _GOOGLE_CLOUD_PRIVATE_KEY_ID: str = get_settings().GOOGLE_CLOUD_PRIVATE_KEY_ID
    _GOOGLE_CLOUD_PRIVATE_KEY: str = get_settings().GOOGLE_CLOUD_PRIVATE_KEY
    _GOOGLE_CLOUD_CLIENT_EMAIL: str = get_settings().GOOGLE_CLOUD_CLIENT_EMAIL
    _GOOGLE_CLOUD_CLIENT_ID: str = get_settings().GOOGLE_CLOUD_CLIENT_ID
    _GOOGLE_CLOUD_CLIENT_X509_CERT_URL: str = get_settings().GOOGLE_CLOUD_CLIENT_X509_CERT_URL
    _GOOGLE_CLOUD_SCOPES: list[str] = ["https://www.googleapis.com/auth/cloud-platform"]

    def __init__(self) -> None:
        self.client = SpeechClient(
            credentials=ServiceAccountCredentials.from_json_keyfile_dict(
                keyfile_dict={
                    "type": GoogleOAuthType.SERVICE_ACCOUNT.value,
                    "project_id": SpeechToTextService._GOOGLE_CLOUD_PROJECT_ID,
                    "private_key_id": SpeechToTextService._GOOGLE_CLOUD_PRIVATE_KEY_ID,
                    "private_key": SpeechToTextService._GOOGLE_CLOUD_PRIVATE_KEY,
                    "client_email": SpeechToTextService._GOOGLE_CLOUD_CLIENT_EMAIL,
                    "client_id": SpeechToTextService._GOOGLE_CLOUD_CLIENT_ID,
                    "auth_uri": GoogleOAuthURI.AUTH.value,
                    "token_uri": GoogleOAuthURI.TOKEN.value,
                    "auth_provider_x509_cert_url": GoogleOAuthURI.AUTH_PROVIDER_X509_CERT_URL.value,
                    "client_x509_cert_url": SpeechToTextService._GOOGLE_CLOUD_CLIENT_X509_CERT_URL,
                },
                scopes=SpeechToTextService._GOOGLE_CLOUD_SCOPES,
            )
        )

    def recognize(self, file: BinaryIO) -> str:
        response: RecognizeResponse = self.client.recognize(
            request=RecognizeRequest(
                config=RecognitionConfig(language_code="ko-KR", model="video"), audio=RecognitionAudio(content=file)
            )
        )
        return response.results.pop().alternatives.pop().transcript
