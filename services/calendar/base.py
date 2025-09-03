from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Dict


class CalendarService(ABC):
    @abstractmethod
    def list_events(self, time_min: datetime, time_max: datetime) -> List[Dict[str, Any]]:
        pass
