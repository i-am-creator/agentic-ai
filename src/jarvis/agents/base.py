from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TaskRequest:
    task_id: str
    content: str


@dataclass
class TaskResponse:
    content: str


class Agent(ABC):
    """Base interface for all agents."""
    def __init__(self, *args, **kwargs):
        """Initialize the agent with any necessary parameters."""
        pass

    @abstractmethod
    def handle(self, request: TaskRequest) -> TaskResponse:
        """Process a task request and return a response."""
        raise NotImplementedError
