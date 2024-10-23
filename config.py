from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: PostgresDsn
    WEBHOOK_PATH: str
    WEBHOOK_URL: str
    SECRET_TOKEN: str


settings = Settings()
