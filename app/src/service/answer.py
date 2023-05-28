from tempfile import NamedTemporaryFile
from typing import Optional

from konlpy.tag import Kkma
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from src.constant import AnswerStatus
from src.custom import AWSS3, Answer
from src.database import CRUDAnswer, get_db
from src.service.aws import AWSS3Service
from src.service.clova import ClovaService
from src.service.google import SpeechToTextService


class AnswerService:
    def __init__(self) -> None:
        self.answer: CRUDAnswer = CRUDAnswer()
        self.s3: AWSS3Service = AWSS3Service()
        self.clova: ClovaService = ClovaService()
        self.google: SpeechToTextService = SpeechToTextService()

    def _soundex_algorithm_korean(self, word: str) -> str:
        """
        To-do
            1. SounDex 알고리즘을 한국어에 적용
        """
        return ""

    def _is_answer(self, word: str, answer_word: str) -> bool:
        """
        To-do
            1. _soundex_algorithm_korean 메서드 사용하여 converted_word 변수 생성
            2. return 문에 converted_word == answer_word 조건 추가
        """
        return word == answer_word

    def _parse_nouns_from_text(self, text: str) -> Optional[set[str]]:
        # parser: Kkma = Kkma()
        # return set(parser.nouns(phrase=text))\
        print("text: ", text)
        if not text:
            return None

        return set(text.split(sep=" "))

    def _compare_all_nouns(self, nouns: Optional[set[str]], answer_word: str) -> AnswerStatus:
        print("nouns: ", nouns)
        if not nouns:
            return AnswerStatus.INCORRECT
        for noun in nouns:
            if self._is_answer(word=noun, answer_word=answer_word):
                return AnswerStatus.CORRECT
        return AnswerStatus.INCORRECT

    def _get_answer_state(self, recognized_text: str, answer_word: str) -> AnswerStatus:
        parsed_nouns: Optional[set[str]] = self._parse_nouns_from_text(text=recognized_text)
        return self._compare_all_nouns(nouns=parsed_nouns, answer_word=answer_word)

    def _grade_recognized_text(self, object_key: str, text: str, db: Session) -> None:
        answer: Answer = self.answer.get_by_object_key(db=db, object_key=object_key)
        print(answer)
        answer_status: AnswerStatus = self._get_answer_state(
            recognized_text=text, answer_word=answer.get("answer_word")
        )
        self.answer.update_state(db=db, answer_id=answer.get("answer_id"), answer_status=answer_status)

    def _recognize_text(self, object_key: str, bucket_name: str) -> str:
        url: HttpUrl = self.s3.get_presigned_url(object_key=object_key, bucket_name=bucket_name)
        return self.clova.recognize_voice_by_external_url(url=url)

        # with NamedTemporaryFile(mode="r+b") as file:
        #     self.s3.download_file(object_key=object_key, bucket_name=bucket_name, file=file)
        #     file.seek(0)
        #     return self.clova.recognize_voice_by_file(file=file)
        # return self.google.recognize(file=file)

    def grade(self, s3_information: AWSS3) -> None:
        db: Session = next(get_db())
        bucket_name: str = s3_information.get("bucket").get("name")
        object_key: str = s3_information.get("object").get("key")
        recognized_text: str = self._recognize_text(object_key=object_key, bucket_name=bucket_name)
        self._grade_recognized_text(object_key=object_key, text=recognized_text, db=db)
