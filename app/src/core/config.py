from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class AWSSettings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_ENDPOINT_URL: Optional[str]


class DatabaseSettings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    @property
    def DATABASE_URL(self) -> str:
        USER_INFORMATION: str = ":".join([self.DATABASE_USER, self.DATABASE_PASSWORD])
        DATABASE_INFORMATION: str = ":".join([self.DATABASE_HOST, self.DATABASE_PORT])
        return f"mysql+mysqldb://{USER_INFORMATION}@{DATABASE_INFORMATION}/{self.DATABASE_NAME}"


class NCPSettings(BaseSettings):
    CLOVA_SPEECH_SECRET_KEY: str
    CLOVA_SPEECH_API_INVOKE_URL: str


class ApplicationSettings(AWSSettings, DatabaseSettings, NCPSettings):
    pass


@lru_cache
def get_settings() -> ApplicationSettings:
    return ApplicationSettings()
