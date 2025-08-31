from fastapi import FastAPI, Request
from config.settings import settings
from services.messenger.telegram import TelegramMessenger

app = FastAPI()

# Dependencies
messenger = TelegramMessenger(token=settings.TELEGRAM_API_TOKEN)


# Webhook endpoint for Telegram
@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()
    chat_id = str(payload["message"]["chat"]["id"])
    incoming_text = messenger.receive_message(payload)

    print(f"Received message: {incoming_text} from chat_id: {chat_id}")

    return {"ok": True}
