"""Minimal workflow execution layer."""

from __future__ import annotations

import asyncio
import uuid
from typing import Optional, Dict, Any

from .context_manager import ContextManager
from .model_selector import ModelSelector
from .agents.code import CodeAgent
from .agents.file import FileAgent
from .agents.base import TaskRequest


class WorkflowManager:
    """Simple manager that routes commands to the appropriate agent."""

    def __init__(self, context_manager: ContextManager, model_config: Optional[Dict[str, Any]] = None) -> None:
        self.context_manager = context_manager
        self.model_selector = ModelSelector(model_type="sllm", model_config=model_config)
        self.agents = {
            "code": CodeAgent(context_manager, self.model_selector),
            "file": FileAgent(context_manager, self.model_selector),
        }

    def _run(self, coro):
        """Utility to execute an async coroutine."""
        return asyncio.run(coro)

    def execute_workflow(self, user_input: str) -> str:
        """Execute a single user request through the agent workflow."""
        task_id = str(uuid.uuid4())
        self._run(self.context_manager.create_task(task_id, user_input))

        agent = self._select_agent(user_input)
        if agent is None:
            return "No suitable agent found for this request"

        request = TaskRequest(task_id=task_id, content=user_input)
        response = agent.handle(request)
        self._run(self.context_manager.add_chunk(task_id, response.content))
        self._run(self.context_manager.update_status(task_id, "completed"))
        return response.content

    def _select_agent(self, user_input: str):
        """Heuristically choose the best agent for the request."""
        lower = user_input.lower()
        if any(k in lower for k in ["explain", "analyze", "code", "function", "class", "method"]):
            return self.agents["code"]
        if any(k in lower for k in ["read", "write", "file", "content", "text"]):
            return self.agents["file"]
        return None
