from __future__ import annotations

from typing import Optional

from .base import Agent, TaskRequest, TaskResponse
from ..services.llm_client import LLMClient


class SummarizerAgent(Agent):
    """Summarize a block of text using an LLM with a fallback."""

    def __init__(self, llm_client: Optional[LLMClient] = None) -> None:
        self.llm = llm_client or LLMClient()

    def handle(self, request: TaskRequest) -> TaskResponse:
        if not request.content:
            return TaskResponse(content="No content to summarize")
            
        prompt = (
            "Summarize the following text in 200 words or less:\n" + request.content
        )
        try:
            summary = self.llm.generate("medium", prompt)
            if not summary:
                # Fallback to a simple truncation if LLM fails
                summary = request.content[:200] + "..." if len(request.content) > 200 else request.content
            return TaskResponse(content=summary)
        except Exception as e:
            # Fallback to a simple truncation if LLM fails
            summary = request.content[:200] + "..." if len(request.content) > 200 else request.content
            return TaskResponse(content=f"Summary (fallback): {summary}")
