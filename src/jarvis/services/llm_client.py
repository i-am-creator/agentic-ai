from __future__ import annotations

from .ollama import OllamaClient
from .bedrock import BedrockClient


class LLMClient:
    def __init__(self) -> None:
        self.ollama = OllamaClient()
        self.bedrock = BedrockClient()

    def generate(self, model: str, prompt: str) -> str:
        if model == "local":
            return self.ollama.generate(prompt)
        return self.bedrock.generate(prompt)
