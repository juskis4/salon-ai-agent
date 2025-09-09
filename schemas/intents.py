from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime


class IntentSchema(BaseModel):
    request_type: Literal["calendar_lookup", "other"] = Field(
        description="Raw description of the the request")
    confidence_score: float = Field(
        description="Confidence score between 0 and 1")
    description: str = Field(
        description="Cleaned description of the request")
    date_start: Optional[datetime] = Field(
        default=None,
        description="Start date and time for the request")
    date_end: Optional[datetime] = Field(
        default=None,
        description="End date and time for the request")
