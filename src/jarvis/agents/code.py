from __future__ import annotations

from pathlib import Path

from .base import Agent, TaskRequest, TaskResponse


class CodeAgent(Agent):
    """Agent that performs very naive code refactoring."""

    def handle(self, request: TaskRequest) -> TaskResponse:
        path_str, _, replacement = request.content.partition(" ")
        path = Path(path_str)
        if not path.exists():
            return TaskResponse(content=f"File {path_str} not found")
        text = path.read_text()
        updated = text.replace("TODO", replacement)
        path.write_text(updated)
        return TaskResponse(content=f"Updated {path_str}")
