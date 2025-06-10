from __future__ import annotations

import requests

class OllamaClient:
    def __init__(self, host: str = "http://localhost:11434") -> None:
        self.host = host

    def generate(self, prompt: str) -> str:
        resp = requests.post(f"{self.host}/api/generate", json={"prompt": prompt})
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "")
