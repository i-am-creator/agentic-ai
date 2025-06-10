from __future__ import annotations

import chromadb

class ChromaVectorStore:
    """Minimal wrapper around Chroma vector store."""

    def __init__(self, path: str = "chroma.db") -> None:
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection("chunks")

    def add(self, doc_id: str, text: str) -> None:
        self.collection.add(documents=[text], ids=[doc_id])

    def query(self, text: str, limit: int = 5) -> list[str]:
        res = self.collection.query(query_texts=[text], n_results=limit)
        return [doc for doc in res.get("documents", [[]])[0]]
