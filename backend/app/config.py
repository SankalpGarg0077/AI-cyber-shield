import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    FIREBASE_CREDENTIALS_PATH: str = "serviceAccountKey.json"

    class Config:
        env_file = ".env"

settings = Settings()