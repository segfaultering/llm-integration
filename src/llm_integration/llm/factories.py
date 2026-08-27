from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from google.genai import Client

from llm_integration.config import settings
from llm_integration.llm.service import GeminiLlmService, StubLlmService


def get_llm() -> Iterator[Client]:
    with Client(api_key=settings.gemini_api_key) as client:
        yield client


def get_llm_service(
    llm: Annotated[Client, Depends(get_llm)],
) -> GeminiLlmService | StubLlmService:
    if settings.llm_stub == 1:
        return StubLlmService()

    return GeminiLlmService(llm)
