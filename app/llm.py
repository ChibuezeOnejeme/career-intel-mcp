from typing import Any

import httpx

from app.config import settings
from app.logging import get_logger

logger = get_logger(__name__)


class LLMProvider:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url=settings.llm_base_url,
            headers={
                "Authorization": f"Bearer {settings.llm_api_key}",
                "Content-Type": "application/json",
            },
            timeout=60.0,
        )

    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        json_mode: bool = False,
    ) -> str:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        body: dict[str, Any] = {
            "model": settings.llm_model,
            "messages": messages,
            "max_tokens": 4096,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}

        try:
            response = await self.client.post("/chat/completions", json=body)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            if not content or content.strip() == "":
                raise ValueError("LLM returned empty content")
            if content.strip().startswith("```json"):
                content = content.strip()[7:]
                if content.endswith("```"):
                    content = content[:-3]
            return content.strip()
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

    async def embed(self, text: str) -> list[float]:
        body = {
            "model": settings.embedding_model,
            "input": text,
        }
        try:
            response = await self.client.post("/embeddings", json=body)
            response.raise_for_status()
            data = response.json()
            return data["data"][0]["embedding"]
        except Exception as e:
            logger.error(f"Embedding call failed: {e}")
            raise

    async def close(self) -> None:
        await self.client.aclose()
