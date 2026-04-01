import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# 实例化配置对象，整个应用都从这里取值
settings = Settings()