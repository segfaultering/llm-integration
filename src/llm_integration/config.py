from dotenv import find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str
    llm_stub: int


settings = Settings(_env_file=find_dotenv())
