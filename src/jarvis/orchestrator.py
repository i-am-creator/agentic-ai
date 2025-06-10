from __future__ import annotations

from typing import Dict, Optional, Any
from .context_manager import ContextManager
from .model_selector import ModelSelector
from .agents.code_agent import CodeAgent
from .agents.file import FileAgent


class TaskOrchestrator:
    """Orchestrates tasks between different agents."""

    def __init__(
        self,
        context_manager: ContextManager,
        model_config: Optional[Dict[str, Any]] = None
    ) -> None:
        self.context_manager = context_manager
        self.model_selector = ModelSelector(
            model_type="sllm",
            model_config=model_config
        )
        self.agents = {
            "code": CodeAgent(context_manager, self.model_selector),
            "file": FileAgent(context_manager, self.model_selector)
        }

    def create_task(self, prompt: str) -> str:
        """Create a new task and return its ID."""
        task_id = self.context_manager.create_task(prompt)
        return task_id

    def handle(self, task_id: str, user_input: str) -> str:
        """Handle a task with the appropriate agent."""
        # Get task context
        task = self.context_manager.get(task_id)
        if not task:
            return "Error: Task not found"

        # Select appropriate agent
        agent = self._select_agent(user_input)
        if not agent:
            return "Error: No suitable agent found for this request"

        # Handle the request
        try:
            response = agent.handle(user_input, task_id)
            self.context_manager.update_status(task_id, "completed")
            return response
        except Exception as e:
            self.context_manager.update_status(task_id, "failed")
            return f"Error: {str(e)}"

    def _select_agent(self, user_input: str) -> Optional[Any]:
        """Select the appropriate agent based on the user input."""
        user_input = user_input.lower()

        # Check for code-related keywords
        code_keywords = ["explain", "analyze", "code", "function", "class", "method"]
        if any(keyword in user_input for keyword in code_keywords):
            return self.agents["code"]

        # Check for file-related keywords
        file_keywords = ["read", "write", "file", "content", "text"]
        if any(keyword in user_input for keyword in file_keywords):
            return self.agents["file"]

        return None

    def list_tasks(self) -> str:
        """List all tasks and their status."""
        tasks = self.context_manager.list_tasks()
        if not tasks:
            return "No tasks found"

        output = []
        for task in tasks:
            output.append(f"Task {task.id}: {task.status}")
            if task.prompt:
                output.append(f"Prompt: {task.prompt}")
            output.append("")

        return "\n".join(output)

    def summarize_task(self, task_id: str) -> str:
        """Generate a summary of a task's history."""
        task = self.context_manager.get(task_id)
        if not task:
            return "Error: Task not found"

        chunks = self.context_manager.get_chunks(task_id)
        if not chunks:
            return "No content found for this task"

        # Use SLLM to generate a summary
        content = "\n".join(chunk.content for chunk in chunks)
        summary = self.model_selector.generate_response(
            f"Summarize the following task history:\n\n{content}",
            system_prompt="You are a helpful assistant that summarizes task histories."
        )

        return summary
