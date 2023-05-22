from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schema.base import Base


class Member(Base):
    mebmer_id: Mapped[int] = mapped_column("mebmer_id", BigInteger, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column("created_at", DateTime(timezone=True), nullable=False)
    age: Mapped[int] = mapped_column("age", Integer, nullable=False)

    question = relationship("Question", secondary="Answer", back_populates="member")
