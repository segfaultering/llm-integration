from typing import Annotated

from fastapi import APIRouter, Depends, status

from llm_integration.llm import LlmService
from llm_integration.schemas import ClfReq, ClfResp
from llm_integration.utils import get_llm_service

router = APIRouter()

LlmServiceDep = Annotated[LlmService, Depends(get_llm_service)]


@router.post(
    "/sentiment-classifier", status_code=status.HTTP_200_OK, response_model=ClfResp
)
def classify_sentiment(text: ClfReq, llm_serv: LlmServiceDep) -> ClfResp:
    return llm_serv.process(text)
