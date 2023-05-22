from sqlalchemy import TextClause, text
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import Executable

from src.constant import AnswerQuery, AnswerStatus
from src.custom import Answer, NotFoundError


class CRUDAnswer:
    def get_by_object_key(self, db: Session, object_key: str) -> Answer:
        with open(file=AnswerQuery.GET_BY_OBJECT_KEY.value) as query:
            get_query: TextClause = text(query.read())

        statement: Executable = get_query.bindparams(object_key=object_key)
        row: Row = db.execute(statement=statement).fetchone()
        db.commit()
        if not row:
            raise NotFoundError(f"{object_key} is not found")
        return row._mapping

    def update_state(self, db: Session, answer_id: int, answer_status: AnswerStatus) -> None:
        with open(file=AnswerQuery.UPDATE_ANSWER_STATUS.value) as query:
            update_query: TextClause = text(query.read())

        statement: Executable = update_query.bindparams(answer_id=answer_id, answer_status=answer_status.value)
        db.execute(statement=statement)
        db.commit()
