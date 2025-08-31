from abc import ABC, abstractmethod


class Messenger(ABC):
    @abstractmethod
    def send_message(self, chat_id: int, text: str) -> None:
        pass

    @abstractmethod
    def receive_message(self, payload: dict) -> str:
        pass
