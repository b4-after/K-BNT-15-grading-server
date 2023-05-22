from enum import Enum
from types import DynamicClassAttribute

from pydantic import FilePath


class AnswerQuery(str, Enum):
    _BASE_PATH: str = "src/sql/answer"
    GET_BY_OBJECT_KEY: str = "get_by_object_key.sql"
    UPDATE_ANSWER_STATUS: str = "update_answer_status.sql"

    @DynamicClassAttribute
    def value(self) -> FilePath:
        return "/".join([AnswerQuery._BASE_PATH, self._value_])


class AnswerStatus(str, Enum):
    BEFORE: str = "BEFORE"
    CORRECT: str = "CORRECT"
    INCORRECT: str = "INCORRECT"


class ForeignKeyConstraint(str, Enum):
    CASCADE: str = "CASCADE"
    SET_NULL: str = "SET NULL"
