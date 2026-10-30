import os
import re
import json
from typing import Any

import httpx

BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
API_KEY = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
DEFAULT_MODEL = os.getenv("LMSTUDIO_MODEL", "local-model")


class LMStudioClient:
    def __init__(self, base_url: str | None = None, api_key: str | None = None, model: str | None = None):
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self.api_key = api_key or API_KEY
        self.model = model or DEFAULT_MODEL

    def ask(self, prompt: str, model: str | None = None, temperature: float = 0.0, max_tokens: int = 512) -> str:
        payload = {
            "model": model or self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
        )
        response.raise_for_status()

        data = response.json()
        if "choices" not in data or not data["choices"]:
            raise ValueError(f"LM Studio returned unexpected payload: {data}")

        content = data["choices"][0]["message"]["content"]
        return str(content)


def clean_json_payload(raw: str) -> dict[str, Any]:
    if raw is None:
        return {}

    text = str(raw).strip()
    text = re.sub(r"```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start : end + 1]

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}
