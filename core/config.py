from typing import Literal
from pydantic.v1 import BaseSettings, ValidationError
from dotenv import load_dotenv

# Load environment variables from the .env file
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

    excluded_routes = [
        "/users/{user_id}",
        '/docs',
        '/openapi.json',
        '/login',
    ]

    ADMIN_USER = {
        "name": "Admin",
        "username": "admin",
        "password": "password",
    }

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

# Try to load the settings and handle validation errors
try:
    settings = Settings()
except ValidationError as e:
    print("Environment variables are missing or invalid:")
    print(e)
    raise e  # Re-raise to stop the application if configuration is incomplete
