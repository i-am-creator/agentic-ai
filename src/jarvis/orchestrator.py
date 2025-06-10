from __future__ import annotations

import uuid

from .context_manager import ContextManager
from .model_selector import ModelSelector
from .agents.base import TaskRequest, TaskResponse
from .agents.system import SystemAgent
from .agents.file import FileAgent
from .agents.code import CodeAgent
from .agents.summarizer import SummarizerAgent
from .utils.chunker import chunk_text
from .services.llm_client import LLMClient


class MultiContextPlanner:
    """Naive orchestrator managing tasks and agents."""

    def __init__(self) -> None:
        self.context_manager = ContextManager()
        self.model_selector = ModelSelector()
        self.system_agent = SystemAgent()
        self.file_agent = FileAgent()
        self.code_agent = CodeAgent()
        self.summarizer_agent = SummarizerAgent()
        self.llm_client = LLMClient()

    def create_task(self, user_input: str) -> str:
        task_id = str(uuid.uuid4())[:8]
        ctx = self.context_manager.get(task_id)
        ctx.history.append(user_input)
        for chunk in chunk_text(user_input):
            self.context_manager.add_chunk(task_id, chunk)
        return task_id

    def handle(self, task_id: str, user_input: str) -> str:
        ctx = self.context_manager.get(task_id)
        ctx.history.append(user_input)
        if not user_input.startswith("!"):
            retrieved = self.context_manager.query_chunks(user_input, limit=3)
        else:
            retrieved = []
        for chunk in chunk_text(user_input):
            self.context_manager.add_chunk(task_id, chunk)
        if retrieved:
            user_input = "\n".join(retrieved) + "\n" + user_input
        model = self.model_selector.select(user_input)
        if user_input.startswith("!sh "):
            req = TaskRequest(task_id, user_input[4:])
            res = self.system_agent.handle(req)
        elif user_input.startswith("!file "):
            req = TaskRequest(task_id, user_input[6:])
            res = self.file_agent.handle(req)
        elif user_input.startswith("!code "):
            req = TaskRequest(task_id, user_input[6:])
            res = self.code_agent.handle(req)
        elif user_input.startswith("!summarize"):
            history = "\n".join(ctx.history)
            req = TaskRequest(task_id, history)
            res = self.summarizer_agent.handle(req)
            self.context_manager.add_summary(task_id, res.content)
        else:
            generated = self.llm_client.generate(model, user_input)
            res = TaskResponse(content=generated)
            ctx.history.append(res.content)
            for chunk in chunk_text(res.content):
                self.context_manager.add_chunk(task_id, chunk)
            return res.content
        ctx.history.append(res.content)
        for chunk in chunk_text(res.content):
            self.context_manager.add_chunk(task_id, chunk)
        return res.content
