from typing import Annotated, Literal, Self

from pydantic import BaseModel, Field, field_validator, model_validator

Sentiment = Annotated[str, Literal["positive", "negative", "neutral", "unsure"]]

CONFIDENCE_FLOOR: float = 0.0
CONFIDENCE_CEIL: float = 1.0
REASON_MAX_LEN: int = 64


class ClfResp(BaseModel):
    sentiment: Sentiment
    confidence: Annotated[float, Field(ge=CONFIDENCE_FLOOR, le=CONFIDENCE_CEIL)]
    second_best: Sentiment
    reason: Annotated[str, Field(max_length=REASON_MAX_LEN)]

    @model_validator(mode="after")
    def check_predictions_differ(self) -> Self:
        if self.sentiment == self.second_best:
            raise ValueError("First and second best classes cannot be the same!")

        return self


class ClfReq(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def is_non_empty(cls, field: str) -> str:
        if not field.split():
            raise ValueError("Request cannot have be an empty string!")

        return field
