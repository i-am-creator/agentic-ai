from __future__ import annotations

from pathlib import Path
from typing import Optional

from .base import Agent, TaskRequest, TaskResponse


class CodeAgent(Agent):
    """Agent that performs code analysis, explanation and refactoring."""

    def __init__(self, context_manager, model_selector, *args, **kwargs) -> None:
        """Create the agent with a context manager and model selector."""
        super().__init__(*args, **kwargs)
        self.context_manager = context_manager
        self.model_selector = model_selector

    def handle(self, request: TaskRequest) -> TaskResponse:
        parts = request.content.split(maxsplit=1)
        if not parts:
            return TaskResponse(content="No command provided")
            
        command = parts[0]
        argument: Optional[str] = parts[1] if len(parts) > 1 else None

        if command == "analyze" and argument:
            return self._analyze_code(argument)
        elif command == "refactor" and argument:
            return self._refactor_code(argument)
        elif command == "explain" and argument:
            return self._explain_code(argument)
        else:
            return TaskResponse(content="Unknown code command. Supported commands: analyze, refactor, explain")

    def _analyze_code(self, file_path: str) -> TaskResponse:
        """Analyze code in a file and provide insights."""
        path = Path(file_path)
        if not path.exists():
            return TaskResponse(content=f"File {file_path} not found")
            
        try:
            text = path.read_text()
            # Basic analysis
            lines = text.splitlines()
            total_lines = len(lines)
            empty_lines = sum(1 for line in lines if not line.strip())
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            code_lines = total_lines - empty_lines - comment_lines
            
            analysis = f"""Code Analysis for {file_path}:
- Total lines: {total_lines}
- Code lines: {code_lines}
- Comment lines: {comment_lines}
- Empty lines: {empty_lines}
- Code to comment ratio: {code_lines/max(comment_lines, 1):.2f}
"""
            return TaskResponse(content=analysis)
        except Exception as e:
            return TaskResponse(content=f"Error analyzing code: {str(e)}")

    def _refactor_code(self, file_path: str) -> TaskResponse:
        """Refactor code in a file."""
        path = Path(file_path)
        if not path.exists():
            return TaskResponse(content=f"File {file_path} not found")
            
        try:
            text = path.read_text()
            # Simple refactoring: replace TODO comments
            updated = text.replace("TODO", "FIXME")
            path.write_text(updated)
            return TaskResponse(content=f"Refactored {file_path}")
        except Exception as e:
            return TaskResponse(content=f"Error refactoring code: {str(e)}")

    def _explain_code(self, file_path: str) -> TaskResponse:
        """Generate an explanation for the given source file."""
        path = Path(file_path)
        if not path.exists():
            return TaskResponse(content=f"File {file_path} not found")

        try:
            code = path.read_text()
        except Exception as e:  # pragma: no cover - file errors
            return TaskResponse(content=f"Error reading file: {str(e)}")

        try:
            explanation = self.model_selector.explain_code(code)
        except Exception as e:  # pragma: no cover - llm failures
            return TaskResponse(content=f"LLM error: {str(e)}")

        return TaskResponse(content=explanation)
