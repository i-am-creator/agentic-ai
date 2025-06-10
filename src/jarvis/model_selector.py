from __future__ import annotations


class ModelSelector:
    """Selects a model based on task complexity."""

    def select(self, text: str) -> str:
        text_lower = text.lower()
        if "hello" in text_lower:
            return "local"
        if "summarize" in text_lower or len(text) < 100:
            return "medium"
        return "heavy"
