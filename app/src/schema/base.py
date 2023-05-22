from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __tablename__(cls: DeclarativeBase):
        return cls.__name__.lower()
