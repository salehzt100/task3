from typing import Literal
from pydantic.v1 import BaseSettings, ValidationError
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ENVIRONMENT: Literal["local", "production"]

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


try:
    settings = Settings()
except ValidationError as e:
    print("Environment variables are missing or invalid:")
    print(e)
    raise e  # Re-raise to stop the application if configuration is incomplete
