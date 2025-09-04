from abc import ABC, abstractmethod
from typing import Any


class Notifier(ABC):
    @abstractmethod
    async def send_message(self, message: str, **kwargs: Any) -> None:
        pass
