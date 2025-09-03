from typing import Optional
from datetime import datetime, timedelta, timezone
from services.llm.base import LLM
from services.calendar.base import CalendarService


class AgentService:
    def __init__(self, llm: LLM, calendar: CalendarService):
        self.llm = llm
        self.calendar = calendar

    async def handle_user_message(self, user_text: str, chat_id: str,
                                  options: Optional[dict] = None,) -> None:

        intent = await self._analyze_intent(user_text, options)

        if intent["intent"] == "calendar_lookup":
            print(f"Intent detected: calendar lookup {chat_id}")
            start, end = self._resolve_date_range(intent["date_range"])
            events = self.calendar.list_events(start, end)
            events_summary = self._format_events(events)

            print(f"sending events_summary: {events_summary}")
            reply = await self.llm.generate(
                prompt=f"""
                User message: {user_text}

                Here are the relevant calendar events ({start.date()} to {end.date()}):
                {events_summary}

                Based on these events, respond helpfully to the user.
                """,
                system="You are a helpful scheduling assistant.",
                options=options
            )
        else:
            print("Intent detected: general")
            reply = await self.llm.generate(
                prompt=user_text,
                system="You are a helpful scheduling assistant.",
                options=options
            )

        return reply

    async def _analyze_intent(self, text: str, options: Optional[dict] = None) -> dict:
        response = await self.llm.generate(
            prompt=f"""
            Classify the user's request into a structured JSON object.

            User message: "{text}"

            Respond ONLY with valid JSON like:
            {{
              "intent": "calendar_lookup" | "general",
              "date_range": "tomorrow" | "next_week" | "last_week" | "unspecified"
            }}
            """,
            system="You are a classifier. Only output strict JSON.",
            options=options
        )

        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"intent": "general", "date_range": "unspecified"}

    def _resolve_date_range(self, label: str) -> tuple[datetime, datetime]:
        now = datetime.now(timezone.utc)
        if label == "tomorrow":
            start = now + timedelta(days=1)
            end = start + timedelta(days=1)
        elif label == "next_week":
            start = now
            end = now + timedelta(days=7)
        elif label == "last_week":
            start = now - timedelta(days=7)
            end = now
        else:
            start = now - timedelta(days=30)
            end = now + timedelta(days=30)
        return start, end

    def _format_events(self, events: list[dict]) -> str:
        if not events:
            return "No events found."

        formatted = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "No title")
            formatted.append(f"- {summary} at {start}")

        return "\n".join(formatted)
