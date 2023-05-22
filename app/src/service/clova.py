import json

from pydantic import HttpUrl
from requests import Session  # type: ignore

from src.constant import ClovaResultType
from src.core import get_settings
from src.custom import ClovaResponse


class ClovaService:
    _X_CLOVASPEECH_API_KEY: str = get_settings().CLOVA_SPEECH_SECRET_KEY
    _CLOVA_SPEECH_API_INVOKE_URL: str = get_settings().CLOVA_SPEECH_API_INVOKE_URL

    def __init__(self) -> None:
        self.session: Session = Session()
        self.session.headers.update(
            {
                "Accept": "application/json;UTF-8",
                "Content-Type": "application/json;UTF-8",
                "X-CLOVASPEECH-API-KEY": ClovaService._X_CLOVASPEECH_API_KEY,
            }
        )

    def _is_succeeded(self, response: ClovaResponse) -> bool:
        return response.get("result") == ClovaResultType.SUCCEEDED.value

    def recognize_voice_by_external_url(self, url: HttpUrl) -> str:
        target_url: HttpUrl = "".join([ClovaService._CLOVA_SPEECH_API_INVOKE_URL, "/recognizer/url"])
        response: ClovaResponse = self.session.post(
            url=target_url,
            data=json.dumps({"url": url, "language": "ko-KR", "completion": "sync"}).encode("UTF-8"),
        ).json()
        print(response)
        if self._is_succeeded(response=response):
            return response.get("text")

        raise ValueError(response.get("message"))
