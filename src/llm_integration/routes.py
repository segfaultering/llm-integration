import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from llm_integration.llm.exceptions import LLMError
from llm_integration.llm.factories import get_llm_service
from llm_integration.llm.service import LlmService
from llm_integration.schemas import ClfReq, ClfResp

logger = logging.getLogger(__name__)

router = APIRouter()

LlmServiceDep = Annotated[LlmService, Depends(get_llm_service)]


@router.post(
    "/sentiment-classifier", status_code=status.HTTP_200_OK, response_model=ClfResp
)
def classify_sentiment(text: ClfReq, llm_serv: LlmServiceDep) -> ClfResp:
    try:
        return llm_serv.process(text)
    except LLMError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="The model was not able to generate a valid output.")
