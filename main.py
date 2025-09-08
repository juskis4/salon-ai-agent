from fastapi import FastAPI, Request
from config.settings import settings
from services.messenger.telegram import TelegramMessenger
from services.llm.openai_llm import OpenAILLM
from services.calendar.google_calendar import GoogleCalendarService
from services.agent.agent_service import AgentService
from services.notifier.twilio_notifier import TwilioNotifier

app = FastAPI()

# Dependencies
messenger = TelegramMessenger(token=settings.TELEGRAM_API_TOKEN)
llm = OpenAILLM(api_key=settings.OPENAI_API_KEY)
calendar = GoogleCalendarService(settings.GOOGLE_SERVICE_ACCOUNT,
                                 settings.GOOGLE_CALENDAR_ID)
notifier = TwilioNotifier(settings.TWILIO_ACCOUNT_SID,
                          settings.TWILIO_AUTH_TOKEN,
                          settings.TWILIO_PHONE_NUMBER)
agent_service = AgentService(llm, calendar)


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()

    chat_id = str(payload.get("message", payload.get(
        "callback_query", {})).get("chat", {}).get("id"))

    incoming_text = messenger.receive_message(payload)

    print(f"Received message: {incoming_text} from chat_id: {chat_id}")

    reply = await agent_service.handle_user_message(
        user_text=incoming_text,
        options={
            "model": settings.DEFAULT_MODEL,
            "temperature": settings.DEFAULT_TEMPERATURE,
            "max_tokens": settings.MAX_TOKENS,
        }
    )

    await messenger.send_message(chat_id, reply)

    # await notifier.send_message(to="+370xxxxxxxx", message="A slot opened up tomorrow at 2PM. Reply YES to book.")
    return {"ok": True}


@app.post("/twilio/webhook")
async def twilio_webhook(request: Request):
    return await notifier.handle_webhook(request)
