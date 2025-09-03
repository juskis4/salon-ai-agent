from datetime import datetime
from services.calendar.base import CalendarService
from typing import List, Dict


class CalendarTools:

    def __init__(self, calendar_service: CalendarService):
        self.calendar = calendar_service

    def list_events(self, time_min: str, time_max: str) -> List[Dict]:
        t_min = datetime.fromisoformat(time_min)
        t_max = datetime.fromisoformat(time_max)
        return self.calendar.list_events(t_min, t_max)
