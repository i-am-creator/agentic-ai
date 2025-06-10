"""Minimal Jarvis-style multi-agent system."""

# Avoid importing heavy dependencies at module import time so that utilities
# like the CLI can run even if optional requirements are missing.
try:  # pragma: no cover - import may fail if dependencies aren't installed
    from .orchestrator import TaskOrchestrator
except Exception:  # pragma: no cover - gracefully handle missing deps
    TaskOrchestrator = None  # type: ignore[assignment]

__all__ = ["TaskOrchestrator"]
