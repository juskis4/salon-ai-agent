import requests
from services.messenger.base import Messenger


class TelegramMessenger(Messenger):
    BASE_URL = "https://api.telegram.org/bot{token}/"

    def __init__(self, token: str):
        self.token = token

    def send_message(self, chat_id: int, text: str) -> None:
        url = self.BASE_URL.format(token=self.token) + "sendMessage"
        payload = {chat_id: chat_id, "text": text}
        response = requests.post(url, json=payload)
        if not response.ok:
            raise Exception(
                f"Failed to send Telegram message: {response.text}")

    def receive_message(self, payload: dict) -> str:
        return payload.get("message", {}).get("text", "")
