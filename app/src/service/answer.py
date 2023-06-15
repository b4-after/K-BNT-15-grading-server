import subprocess
from tempfile import NamedTemporaryFile
from typing import Optional

from konlpy.tag import Kkma
from sqlalchemy.orm import Session

from src.constant import AnswerStatus
from src.custom import AWSS3, Answer, ClovaBoostingKeywords
from src.database import CRUDAnswer, CRUDQuestion, get_db
from src.service.aws import AWSS3Service
from src.service.clova import ClovaService
from src.service.google import SpeechToTextService
from src.util import soundex


class AnswerService:
    def __init__(self) -> None:
        self.answer: CRUDAnswer = CRUDAnswer()
        self.question: CRUDQuestion = CRUDQuestion()
        self.s3: AWSS3Service = AWSS3Service()
        self.clova: ClovaService = ClovaService()
        self.google: SpeechToTextService = SpeechToTextService()

    def _is_answer(self, word: str, answer_words: list[str]) -> bool:
        return word in answer_words or soundex(word) in answer_words

    def _parse_nouns_from_text(self, text: str) -> Optional[set[str]]:
        parser: Kkma = Kkma()
        return set(parser.nouns(phrase=text))

    def _compare_all_nouns(self, nouns: Optional[set[str]], answer_words: list[str]) -> AnswerStatus:
        print("nouns: ", nouns)
        if not nouns:
            return AnswerStatus.INCORRECT
        for noun in nouns:
            if self._is_answer(word=noun, answer_words=answer_words):
                return AnswerStatus.CORRECT
        return AnswerStatus.INCORRECT

    def _get_answer_state(self, recognized_text: str, answer_words: list[str]) -> AnswerStatus:
        parsed_nouns: Optional[set[str]] = self._parse_nouns_from_text(text=recognized_text)
        return self._compare_all_nouns(nouns=parsed_nouns, answer_words=answer_words)

    def _get_boosting_keywords(self, db: Session) -> list[ClovaBoostingKeywords]:
        return [
            ClovaBoostingKeywords(words=question.get("word"))
            for question in self.question.get_all_over_two_characters(db=db)
        ]

    def _grade_recognized_text(self, object_key: str, text: str, db: Session) -> None:
        answer: Answer = self.answer.get_by_object_key(db=db, object_key=object_key)
        print(answer)
        answer_status: AnswerStatus = self._get_answer_state(
            recognized_text=text, answer_words=answer.get("answer_words")
        )
        self.answer.update_state(db=db, answer_id=answer.get("answer_id"), answer_status=answer_status)

    def _recognize_text(self, db: Session, object_key: str, bucket_name: str) -> str:
        boosting_keywords: list[ClovaBoostingKeywords] = self._get_boosting_keywords(db=db)
        with NamedTemporaryFile(mode="r+b", suffix=".webm") as webm_file:
            self.s3.download_file(object_key=object_key, bucket_name=bucket_name, file=webm_file)
            with NamedTemporaryFile(mode="r+b", suffix=".wav") as wav_file:
                subprocess.run(["./ffmpeg", "-y", "-i", webm_file.name, wav_file.name], check=True)
                # self.s3.upload_file(object_key=wav_file.name, bucket_name=bucket_name, file=wav_file)
                wav_file.seek(0)
                return self.clova.recognize_voice_by_file(file=wav_file, boosting_keywords=boosting_keywords)

    def grade(self, s3_information: AWSS3) -> None:
        db: Session = next(get_db())
        bucket_name: str = s3_information.get("bucket").get("name")
        object_key: str = s3_information.get("object").get("key")
        recognized_text: str = self._recognize_text(object_key=object_key, bucket_name=bucket_name, db=db)
        self._grade_recognized_text(object_key=object_key, text=recognized_text, db=db)
