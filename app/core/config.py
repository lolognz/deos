import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    download_dir: str = os.getenv("DOWNLOAD_DIR", "data/downloads")
    env_name: str = os.getenv("ENV_NAME", "development")


settings = Settings()
