from .base import CalendarService
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
from typing import Any, List, Dict

from datetime import datetime, timezone


class GoogleCalendarService(CalendarService):
    def __init__(self, credentials_file: str, calendar_id: str = "primary"):
        creds = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=["https://www.googleapis.com/auth/calendar.readonly"]
        )
        print(creds)
        self.service = build("calendar", "v3", credentials=creds)
        self.calendar_id = calendar_id

    def to_rfc3339(self, dt: datetime) -> str:
        return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()

    def list_events(self, time_min: datetime, time_max: datetime) -> List[Dict[str, Any]]:

        start = self.to_rfc3339(time_min)
        end = self.to_rfc3339(time_max)

        events_result = self.service.events().list(
            calendarId=self.calendar_id,
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        return events_result.get("items", [])
