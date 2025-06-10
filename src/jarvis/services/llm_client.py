from __future__ import annotations

from typing import Optional
from functools import lru_cache

from langchain_community.chat_models import BedrockChat
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from .ollama import OllamaClient
from .bedrock import BedrockClient


class LLMClient:
    """Unified LLM client using LangChain for model integration."""

    @staticmethod
    @lru_cache(maxsize=1)
    def _initialize_bedrock() -> BedrockChat:
        """Initialize BedrockChat client with caching."""
        return BedrockChat(
            model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
            region_name="us-east-1",
            model_kwargs={"temperature": 0.7, "max_tokens": 8000},
        )

    def __init__(self) -> None:
        # Initialize legacy clients for backward compatibility
        self.ollama = OllamaClient()
        self.bedrock = BedrockClient()

        # Initialize LangChain models
        self._init_langchain_models()

    def _init_langchain_models(self) -> None:
        """Initialize LangChain models with appropriate configurations."""
        try:
            # Initialize Bedrock models
            bedrock_client = self._initialize_bedrock()
            self.medium_model = self.heavy_model = bedrock_client

        except Exception as e:
            print(f"Warning: Model initialization failed - {str(e)}")
            self.medium_model = self.heavy_model = None

    def generate(self, model: str, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text using the specified model with optional system prompt."""
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        try:
            if model == "local":
                return self.ollama.generate(prompt)
            elif model in ("medium", "heavy") and self.medium_model:
                response = self.medium_model.invoke(messages)
                return response.content
            else:
                raise ValueError(f"Model {model} not available")

        except Exception as e:
            print(f"Warning: LangChain model failed - {str(e)}")
            # Fallback to legacy client
            return self.bedrock.generate(prompt)

    def refresh_bedrock_client(self) -> None:
        """Force refresh the Bedrock client if needed."""
        self._initialize_bedrock.cache_clear()
        self._init_langchain_models()