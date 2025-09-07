from pydantic import BaseModel, Field


class IntentSchema(BaseModel):
    description: str = Field(
        description="Raw description of the the request")
    is_calendar_event: bool = Field(
        description="Whether this text describes a calendar event or events")
    confidence_score: float = Field(
        description="Confidence score between 0 and 1")
