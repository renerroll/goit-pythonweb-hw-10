from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    FRONTEND_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
