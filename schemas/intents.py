from pydantic import BaseModel, Field
from typing import Literal


class IntentSchema(BaseModel):
    request_type: Literal["calendar_lookup", "other"] = Field(
        description="Raw description of the the request")
    confidence_score: float = Field(
        description="Confidence score between 0 and 1")
    description: str = Field(
        description="Cleaned description of the request")
