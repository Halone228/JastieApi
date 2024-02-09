from pydantic_settings import BaseSettings, SettingsConfigDict
from os import getenv


class AppConfig(BaseSettings):
    ALLOWED_CHATS: list[int]

    model_config = SettingsConfigDict(
        env_file='.env.local' if getenv("DEV") else '.env',
        extra='allow'
    )


config = AppConfig()


__all__ = [
    'config'
]