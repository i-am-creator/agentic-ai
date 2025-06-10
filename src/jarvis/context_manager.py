from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Iterable

from .db import Base, Task, Chunk, Summary, get_engine, get_sessionmaker
from .vector_store import ChromaVectorStore


@dataclass
class Context:
    task_id: str
    history: List[str] = field(default_factory=list)


class ContextManager:
    """Stores context for multiple tasks in SQLite and Chroma."""

    def __init__(self, db_url: str = "sqlite:///jarvis.db") -> None:
        self.engine = get_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = get_sessionmaker(self.engine)
        self.vector_store = ChromaVectorStore()
        self.contexts: Dict[str, Context] = {}

    def _ensure_task(self, session, task_id: str) -> None:
        if not session.get(Task, task_id):
            session.add(Task(id=task_id))
            session.commit()

    def get(self, task_id: str) -> Context:
        if task_id not in self.contexts:
            self.contexts[task_id] = Context(task_id)
        return self.contexts[task_id]

    def add_chunk(self, task_id: str, content: str) -> None:
        session = self.SessionLocal()
        self._ensure_task(session, task_id)
        session.add(Chunk(task_id=task_id, content=content))
        self.vector_store.add(f"{task_id}-{len(content)}", content)
        session.commit()
        session.close()

    def get_chunks(self, task_id: str, limit: int = 5) -> Iterable[str]:
        session = self.SessionLocal()
        chunks = (
            session.query(Chunk)
            .filter(Chunk.task_id == task_id)
            .order_by(Chunk.id.desc())
            .limit(limit)
            .all()
        )
        texts = [c.content for c in chunks]
        session.close()
        return texts

    def query_chunks(self, text: str, limit: int = 5) -> Iterable[str]:
        return self.vector_store.query(text, limit)

    def add_summary(self, task_id: str, content: str) -> None:
        session = self.SessionLocal()
        self._ensure_task(session, task_id)
        session.add(Summary(task_id=task_id, content=content))
        session.commit()
        session.close()
