from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DEFAULT_MODEL: str
    MAX_TOKENS: int
    DEFAULT_TEMPERATURE: float

    TELEGRAM_API_TOKEN: str

    GOOGLE_SERVICE_ACCOUNT: str
    GOOGLE_CALENDAR_ID: str

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    class Config:
        env_file = ".env"


settings = Settings()
