import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    gemini_api_key: str
    port: int = 8000
    host: str = "127.0.0.1"

    # extra="ignore" разрешает иметь лишние переменные в .env и не валить скрипт
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH, 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

if __name__ == "__main__":
    print("Ключ Gemini загружен успешно:", settings.gemini_api_key[:10] + "...")