from fastapi import FastAPI, Request
from config.settings import settings
from services.messenger.telegram import TelegramMessenger
from services.llm.openai_llm import OpenAILLM
from services.agent.agent_service import AgentService

app = FastAPI()

# Dependencies
messenger = TelegramMessenger(token=settings.TELEGRAM_API_TOKEN)
llm = OpenAILLM(api_key=settings.OPENAI_API_KEY)

agent_service = AgentService(llm=llm)


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()
    chat_id = str(payload["message"]["chat"]["id"])
    incoming_text = messenger.receive_message(payload)

    print(f"Received message: {incoming_text} from chat_id: {chat_id}")

    reply = await agent_service.handle_user_message(
        user_text=incoming_text,
        chat_id=chat_id,
        options={
            "model": settings.DEFAULT_MODEL,
            "temperature": settings.DEFAULT_TEMPERATURE,
            "max_tokens": settings.MAX_TOKENS,
        }
    )

    messenger.send_message(chat_id, reply)

    return {"ok": True}
