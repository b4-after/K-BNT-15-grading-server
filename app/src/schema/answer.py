from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.constant import ForeignKeyConstraint
from src.schema.base import Base


class Answer(Base):
    answer_id: Mapped[BigInteger] = mapped_column("answer_id", BigInteger, primary_key=True, autoincrement=True)
    member_id: Mapped[BigInteger] = mapped_column(
        "member_id",
        BigInteger,
        ForeignKey(
            "member.member_id",
            onupdate=ForeignKeyConstraint.CASCADE.value,
            ondelete=ForeignKeyConstraint.SET_NULL.value,
        ),
        nullable=False,
    )
    question_id: Mapped[BigInteger] = mapped_column(
        "question_id",
        BigInteger,
        ForeignKey(
            "question.question_id",
            onupdate=ForeignKeyConstraint.CASCADE.value,
            ondelete=ForeignKeyConstraint.SET_NULL.value,
        ),
        nullable=False,
    )
    answer_state: Mapped[str] = mapped_column("answer_state", String(length=8), nullable=False, default="BEFORE")
    audio_url: Mapped[str] = mapped_column("audio_url", String(length=255), nullable=False)
