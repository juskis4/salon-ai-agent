from .base import Notifier
from twilio.rest import Client
from fastapi import Request


class TwilioNotifier(Notifier):
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

    async def send_message(self, to: str, message: str, **kwargs) -> None:
        self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=to
        )

    async def handle_webhook(self, request: Request) -> dict:
        form = await request.form()
        from_number = form.get("From")
        body = form.get("Body")

        print(f"Received SMS from {from_number}: {body}")

        return {"status": "received"}
