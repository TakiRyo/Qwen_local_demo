from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import httpx


class VLMError(RuntimeError):
    pass


@dataclass
class VLMClient:
    base_url: str
    timeout_sec: float = 60.0

    async def list_models(self) -> List[str]:
        url = f"{self.base_url}/v1/models"
        async with httpx.AsyncClient(timeout=self.timeout_sec) as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise VLMError(f"Model list failed: {response.status_code} {response.text}")
        data = response.json()
        return [item["id"] for item in data.get("data", [])]

    async def resolve_model(self, model_name: Optional[str]) -> str:
        if model_name:
            return model_name
        models = await self.list_models()
        if not models:
            raise VLMError("No models returned from vLLM server")
        return models[0]

    async def chat(self, *, messages: List[dict], model_name: Optional[str], max_tokens: int) -> str:
        model = await self.resolve_model(model_name)
        url = f"{self.base_url}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
        }
        async with httpx.AsyncClient(timeout=self.timeout_sec) as client:
            response = await client.post(url, json=payload)
        if response.status_code != 200:
            raise VLMError(f"Chat request failed: {response.status_code} {response.text}")
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise VLMError(f"Unexpected response format: {data}") from exc
