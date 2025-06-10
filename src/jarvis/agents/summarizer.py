from __future__ import annotations

from .base import Agent, TaskRequest, TaskResponse


class SummarizerAgent(Agent):
    """Very naive summarizer that truncates text to first 200 characters."""

    def handle(self, request: TaskRequest) -> TaskResponse:
        summary = request.content[:200]
        return TaskResponse(content=summary)
