from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from .base import Agent, TaskRequest, TaskResponse


class FileAgent(Agent):
    """Agent for simple file operations."""

    def handle(self, request: TaskRequest) -> TaskResponse:
        parts = request.content.split(maxsplit=1)
        if not parts:
            return TaskResponse(content="No command provided")
        command = parts[0]
        argument: Optional[str] = parts[1] if len(parts) > 1 else None

        if command == "read" and argument:
            path = Path(argument)
            if not path.exists():
                return TaskResponse(content=f"File {argument} not found")
            return TaskResponse(content=path.read_text())
        if command == "write" and argument:
            name, _, body = argument.partition(" ")
            Path(name).write_text(body)
            return TaskResponse(content=f"Wrote to {name}")
        return TaskResponse(content="Unknown file command")
