from typing import Optional
from datetime import datetime
from services.llm.base import LLM
from services.calendar.base import CalendarService
from schemas.intents import IntentSchema
from schemas.calendar import ScheduleResponseSchema


class AgentService:
    def __init__(self, llm: LLM, calendar: CalendarService):
        self.llm = llm
        self.calendar = calendar

    async def handle_user_message(self, user_text: str,
                                  options: Optional[dict] = None,) -> None:

        eventInfo = await self.extract_event_info(
            user_text=user_text,
            options=options
        )
        print(f"Event info: {eventInfo}")

        if eventInfo.confidence_score < 0.7:
            print(f"Low confidence score: {eventInfo.confidence_score}")
            return None

        if eventInfo.request_type == "calendar_lookup":
            return await self.handle_calendar_lookup(eventInfo.description, options)
        else:
            print("Request type not supported")
            return None

    async def extract_event_info(self, user_text: str, options: Optional[dict] = None) -> IntentSchema:
        print("Starting event extraction analysis")

        response = await self.llm.generate_parse(
            user_input=user_text,
            system="Analyze if the text describes a calendar lookup.",
            options=options,
            schema=IntentSchema
        )

        print(
            f"Extraction complete - Request type: {response.request_type}, Confidence: {response.confidence_score:.2f}")
        return response

    async def handle_calendar_lookup(self, description: str, options: Optional[dict] = None) -> str:
        print("Processing calendar lookup request")

        today = datetime.now()
        date_context = f"Today is {today.strftime('%A, %B %d, %Y')}."

        response = await self.llm.generate_parse(
            user_input=description,
            system=f"{date_context} Extract the date range and lookup the user's calendar events for that range. Returns days with appointments only.",
            options=options,
            schema=ScheduleResponseSchema
        )
        print(
            f"calendar lookup complete: {response.days} days")
        return self.format_schedule(response)

    def format_schedule(self, schedule: ScheduleResponseSchema) -> str:
        lines = []
        for day in schedule.days:
            lines.append(f"- {day.date}")
            if not day.appointments:
                lines.append("  (No appointments)")
            else:
                for appt in day.appointments:
                    lines.append(
                        f"  - {appt.time}: {appt.client} - {appt.service}")
            lines.append("")  # blank line between days
        return "\n".join(lines).strip()
