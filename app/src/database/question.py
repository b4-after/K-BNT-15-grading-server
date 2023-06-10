from typing import Sequence

from sqlalchemy import text
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import Executable

from src.custom import NotFoundError, Question


class CRUDQuestion:
    def get_all_over_two_characters(self, db: Session) -> list[Question]:
        statement: Executable = text(
            text="""
                SELECT
                    word
                FROM (
                    SELECT
                        word
                    FROM question
                    UNION ALL
                    SELECT
                        synonym_word AS word
                    FROM synonym
                ) AS target_word
                WHERE CHAR_LENGTH(word) > 1;
            """
        )
        rows: Sequence[Row] = db.execute(statement=statement).fetchall()
        db.commit()
        if not rows:
            raise NotFoundError("questions not found")
        return [row._mapping for row in rows]
