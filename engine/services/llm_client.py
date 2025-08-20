import httpx
import os
from engine.core.config import settings


class LLMClient:
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.api_url = settings.LLM_API_URL
        self.model = settings.LLM_MODEL

    async def ask(self, prompt: str) -> str:
        """Send a prompt to OpenRouter and return the response"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant for interview automation.",
                },
                {"role": "user", "content": prompt},
            ],
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(self.api_url, headers=headers, json=payload)

        response.raise_for_status()
        data = response.json()

        # Extract the answer
        return data["choices"][0]["message"]["content"]
