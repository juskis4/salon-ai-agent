from pydantic import BaseModel, Field
from typing import List


class AppointmentSchema(BaseModel):
    time: str = Field(
        description="Time of the appointment in human-readable format, e.g. '08:00 AM'"
    )
    client: str = Field(description="Name of the client")
    service: str = Field(description="Service description")


class DayScheduleSchema(BaseModel):
    date: str = Field(
        description="Date of the appointments in human-readable format, e.g. 'August 20, 2025'"
    )
    appointments: List[AppointmentSchema] = Field(
        description="List of appointments for this date"
    )


class ScheduleResponseSchema(BaseModel):
    days: List[DayScheduleSchema] = Field(
        description="List of days, each containing its appointments"
    )
