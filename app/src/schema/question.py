from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schema.base import Base


class Question(Base):
    question_id: Mapped[int] = mapped_column("question_id", BigInteger, primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column("word", String(length=8), nullable=False)
    image_url: Mapped[str] = mapped_column("image_url", String(length=256), nullable=False)

    member = relationship("Member", secondary="Answer", back_populates="question")
