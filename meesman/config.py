from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MEESMAN_",
        env_file=".env",
        extra="ignore",
    )

    api_base_url: str = "https://public-api.meesman.nl/"
    session_file: Path = Path("data/session.json")


settings = Settings()
