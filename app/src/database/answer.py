from sqlalchemy import TextClause, text
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import Executable

from src.constant import AnswerQuery, AnswerStatus
from src.custom import Answer, NotFoundError


class CRUDAnswer:
    def get_by_object_key(self, db: Session, object_key: str) -> Answer:
        # with open(file=AnswerQuery.GET_BY_OBJECT_KEY.value) as query:
        #     get_query: TextClause = text(query.read())

        statement: Executable = text(
            text="""
                WITH cte (answer_id, question_id) AS (
                    SELECT
                        answer_id,
                        question_id
                    FROM answer
                    WHERE audio_file_object_key = :object_key
                )

                SELECT
                    answer_id,
                    JSON_ARRAYAGG(word) AS answer_words
                FROM (
                    SELECT
                        cte.answer_id AS answer_id,
                        question.word AS word
                    FROM cte
                    JOIN question
                    USING (question_id)
                    UNION ALL
                    SELECT
                        cte.answer_id AS answer_id,
                        synonym.synonym_word AS word
                    FROM cte
                    JOIN synonym
                    USING (question_id)
                ) AS target_answer;
            """
        ).bindparams(object_key=object_key)
        row: Row = db.execute(statement=statement).fetchone()
        db.commit()
        if not row:
            raise NotFoundError(f"{object_key} is not found")
        return row._mapping

    def update_state(self, db: Session, answer_id: int, answer_status: AnswerStatus) -> None:
        # with open(file=AnswerQuery.UPDATE_ANSWER_STATUS.value) as query:
        #     update_query: TextClause = text(query.read())

        statement: Executable = text(
            text="""
                UPDATE answer
                SET answer_status = :answer_status
                WHERE answer_id = :answer_id;
            """
        ).bindparams(answer_id=answer_id, answer_status=answer_status.value)
        db.execute(statement=statement)
        db.commit()
