import logging
from typing import Protocol

from google.genai import Client, types
from pydantic import ValidationError

from llm_integration.config import settings
from llm_integration.llm.exceptions import LLMError
from llm_integration.llm.utils import get_sys_prompt, make_repair_prompt
from llm_integration.schemas import ClfReq, ClfResp

logger = logging.getLogger(__name__)


class LlmService(Protocol):
    def process(self, request: ClfReq) -> ClfResp: ...


class GeminiLlmService:
    def __init__(self, client: Client) -> None:
        self.client = client

    def process(self, request: ClfReq) -> ClfResp:
        response = self.client.models.generate_content(
            model=settings.model,
            contents=request.text,
            config=types.GenerateContentConfig(
                system_instruction=get_sys_prompt(), temperature=settings.temp
            ),
        )

        assert response is not None

        try:
            return ClfResp.model_validate_json(response.text)

        except ValidationError as err:
            sys_prompt, user_prompt = make_repair_prompt(
                get_sys_prompt(), request.text, err
            )

            try:
                repair_resp = self.client.models.generate_content(
                    model=settings.model,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=sys_prompt, temperature=settings.temp
                    ),
                )

                assert repair_resp is not None

                return ClfResp.model_validate_json(repair_resp.text)

            except ValidationError:
                logger.exception(""" 
                    USER_PROMPT:\n%s\nSYS_PROMPT:\n%s\nOUTPUT:\n%s
                """, user_prompt, sys_prompt, repair_resp.text)
                raise LLMError("Repair prompt failure!")

        return ClfResp.model_validate_json(response.text)


class StubLlmService:
    def process(self, request: ClfReq) -> ClfResp:
        return ClfResp(
            sentiment="neutral",
            confidence=0.6,
            second_best="unsure",
            reason="No clear context.",
        )
