from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OPENAI_API_KEY: str
    TELEGRAM_API_TOKEN: str
    # GOOGLE_CREDENTIALS_FILE: str

    class Config:
        env_file = ".env"


settings = Settings()
