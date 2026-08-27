from typing import Protocol

from llm_integration.schemas import ClfReq, ClfResp


class LlmService(Protocol):
    def process(self, request: ClfReq) -> ClfResp: ...


class GeminiLlmService:
    def __init__(self, client) -> None:
        self.client = client

    def process(self, request: ClfReq) -> ClfResp:
        raise NotImplementedError()


class StubLlmService:
    def process(self, request: ClfReq) -> ClfResp:
        return ClfResp(
            sentiment="neutral",
            confidence=0.6,
            second_best="unsure",
            reason="No clear context.",
        )
