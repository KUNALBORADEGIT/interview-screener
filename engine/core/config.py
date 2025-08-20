from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_url: str

    LLM_API_KEY: str
    LLM_API_URL: str = "https://openrouter.ai/api/v1/chat/completions"
    LLM_MODEL: str = "mistralai/mixtral-8x7b-instruct"

    SERVICE_URL: str

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    LOG_DIR: str = str(Path(__file__).parent.parent / "logs")

    # BASE_DIR: str = str(Path(__file__).parent.parent.resolve())
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent.parent)

    class Config:
        env_file = ".env"


settings = Settings()
