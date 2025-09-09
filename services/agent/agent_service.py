from pyparsing import Any
from services.llm.base import LLM
from services.calendar.base import CalendarService
from schemas.intents import IntentSchema
from schemas.calendar import ScheduleResponseSchema
from typing import Optional
from datetime import datetime


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

        if eventInfo.confidence_score < 0.7:
            print(f"Low confidence score: {eventInfo.confidence_score}")
            return None

        if eventInfo.request_type == "calendar_lookup":
            if eventInfo.date_start and eventInfo.date_end:
                events = self.calendar.list_events(
                    eventInfo.date_start, eventInfo.date_end)
                return await self.handle_calendar_lookup(eventInfo.description, events, options)
        else:
            print("Request type not supported")
            return None

    async def extract_event_info(self, user_text: str, options: Optional[dict] = None) -> IntentSchema:
        print("Starting event extraction analysis")

        today = datetime.now()
        date_context = f"Today is {today.strftime('%A, %B %d, %Y')}."

        response = await self.llm.generate_parse(
            user_input=user_text,
            system=f"{date_context}Analyze if the text describes a calendar lookup and extract relevant info.",
            options=options,
            schema=IntentSchema
        )

        print(
            f"Extraction complete - Request type: {response.request_type}, Confidence: {response.confidence_score:.2f}")
        return response

    async def handle_calendar_lookup(self, description: str, events: Any, options: Optional[dict] = None) -> str:
        print("Processing calendar lookup request")

        today = datetime.now()
        date_context = f"Today is {today.strftime('%A, %B %d, %Y')}."

        response = await self.llm.generate_parse(
            user_input=description,
            system=f"""{date_context}

                Here are the relevant calendar events:{events}

                Based on these events, respond helpfully to the user.""",
            options=options,
            schema=ScheduleResponseSchema
        )

        return self._format_schedule(response)

    def _format_schedule(self, schedule: ScheduleResponseSchema) -> str:
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
