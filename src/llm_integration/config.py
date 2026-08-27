from pathlib import Path

from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str
    llm_stub: int
    app_root: Path
    model: str
    temp: float


settings = Settings(_env_file=find_dotenv())
