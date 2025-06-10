from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True)
    prompt = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    chunks = relationship("Chunk", back_populates="task")
    summaries = relationship("Summary", back_populates="task")


class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, ForeignKey("tasks.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    task = relationship("Task", back_populates="chunks")


class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, ForeignKey("tasks.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    task = relationship("Task", back_populates="summaries")


def get_engine(url: str = "sqlite:///jarvis.db"):
    return create_engine(url, future=True)


def get_sessionmaker(engine):
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)
