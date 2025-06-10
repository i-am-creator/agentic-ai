from __future__ import annotations

def chunk_text(text: str, size: int = 1024) -> list[str]:
    """Split text into roughly size-byte chunks."""
    return [text[i : i + size] for i in range(0, len(text), size)]
