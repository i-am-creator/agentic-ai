from __future__ import annotations

from typing import List, Optional
from datetime import datetime

from sqlmodel import Field, Session, SQLModel, create_engine, select

from .db import Base, Task, Chunk, Summary, get_engine, get_sessionmaker


class Context(SQLModel):
    """In-memory context for a task."""
    task_id: str
    history: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ContextManager:
    """Simplified context manager using only SQLite."""

    def __init__(self, db_url: str = "sqlite:///jarvis.db") -> None:
        # Initialize SQLModel
        self.engine = get_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = get_sessionmaker(self.engine)

    def _ensure_task(self, session: Session, task_id: str, prompt: str | None = None) -> None:
        if not session.get(Task, task_id):
            session.add(Task(id=task_id, prompt=prompt or "", status="pending"))
            session.commit()

    async def create_task(self, task_id: str, prompt: str) -> None:
        """Create a new task."""
        session = self.SessionLocal()
        self._ensure_task(session, task_id, prompt)
        session.close()

    async def update_status(self, task_id: str, status: str) -> None:
        """Update task status."""
        session = self.SessionLocal()
        task = session.get(Task, task_id)
        if task:
            task.status = status
            session.commit()
        session.close()

    async def get(self, task_id: str) -> Context:
        """Get task context."""
        session = self.SessionLocal()
        task = session.get(Task, task_id)
        if not task:
            session.close()
            raise ValueError(f"Task with ID {task_id} not found")
        
        # Load history from chunks
        chunks = session.execute(
            select(Chunk)
            .where(Chunk.task_id == task_id)
            .order_by(Chunk.id)
        ).scalars().all()
        
        context = Context(
            task_id=task_id,
            history=[c.content for c in chunks]
        )
        session.close()
        return context

    async def add_chunk(self, task_id: str, content: str) -> None:
        """Add a chunk of content to the task."""
        session = self.SessionLocal()
        self._ensure_task(session, task_id)
        
        # Add to database
        session.add(Chunk(task_id=task_id, content=content))
        session.commit()
        session.close()

    async def get_task_history(self, task_id: str) -> List[str]:
        """Get task history."""
        session = self.SessionLocal()
        chunks = session.execute(
            select(Chunk)
            .where(Chunk.task_id == task_id)
            .order_by(Chunk.id)
        ).scalars().all()
        history = [c.content for c in chunks]
        session.close()
        return history

    async def add_summary(self, task_id: str, content: str) -> None:
        """Add a summary to the task."""
        session = self.SessionLocal()
        self._ensure_task(session, task_id)
        session.add(Summary(task_id=task_id, content=content))
        session.commit()
        session.close()

    async def list_tasks(self, status: str | None = None) -> list[Task]:
        """List all tasks."""
        session = self.SessionLocal()
        query = select(Task)
        if status is not None:
            query = query.where(Task.status == status)
        tasks = session.execute(query).scalars().all()
        session.close()
        return tasks

    async def get_chunks(self, task_id: str) -> list[Chunk]:
        """Return all chunk records for a task."""
        session = self.SessionLocal()
        records = session.execute(
            select(Chunk).where(Chunk.task_id == task_id).order_by(Chunk.id)
        ).scalars().all()
        session.close()
        return records

    def get_task_record(self, task_id: str) -> Task | None:
        """Return the raw task database record."""
        session = self.SessionLocal()
        task = session.get(Task, task_id)
        session.close()
        return task
