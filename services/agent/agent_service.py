from services.llm.base import LLM
from typing import Optional


class AgentService:

    def __init__(self, llm: LLM):
        self.llm = llm

    async def handle_user_message(
        self,
        user_text: str,
        chat_id: str,
        system_prompt: Optional[str] = None,
        options: Optional[dict] = None,
    ) -> str:

        print(f"Received message: {user_text} from chat_id: {chat_id}")

        system_prompt = system_prompt or "You are a helpful salon scheduling assistant."

        reply = await self.llm.generate(
            prompt=user_text,
            system=system_prompt,
            options=options
        )

        return reply
