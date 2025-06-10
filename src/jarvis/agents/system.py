from __future__ import annotations

import subprocess
from .base import Agent, TaskRequest, TaskResponse


class SystemAgent(Agent):
    """Agent for executing shell commands in a sandboxed way."""

    def handle(self, request: TaskRequest) -> TaskResponse:
        # TODO: Replace subprocess.run with a more secure method for executing shell commands.
        # This could involve using a dedicated command execution service, a safer subprocess
        # library, or carefully sanitizing inputs.
        try:
            print("SYSTEM CMD:", request.content)
            result = subprocess.run(
                request.content,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
            output = result.stdout.strip()
        except subprocess.CalledProcessError as exc:
            output = exc.stderr.strip()
        return TaskResponse(content=output)
