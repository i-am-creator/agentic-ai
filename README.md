# Agentic AI

This repository contains a minimal proof-of-concept implementation of a
"Jarvis"-style multi-agent assistant. The design is inspired by the
planning document provided in the prompt and focuses on a simple command
line interface that coordinates different agents.

An experimental FastAPI server exposes the same functionality over HTTP.

## Features

* **MultiContextPlanner** orchestrates tasks and keeps history per task in
  SQLite.
* **ModelSelector** chooses between three model classes: `local`, `medium`
  and `heavy` (heuristic based).
* **Vector store** persists chunks to Chroma and allows retrieval of top-k
  relevant snippets.
* **Agents**
  * `SystemAgent` runs shell commands.
  * `FileAgent` performs basic file reads and writes.
  * `CodeAgent` does a trivial text substitution to simulate refactoring.
  * `SummarizerAgent` truncates logs to 200 characters.

## Usage

Create a virtual environment with Python 3.10+ and install the project in
editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the CLI with a command. Prefixes select agents:

```bash
python -m jarvis.cli !sh ls
python -m jarvis.cli !file read README.md
python -m jarvis.cli !code path/to/file.py replacement
python -m jarvis.cli !summarize
```

Anything that does not start with `!sh`, `!file`, `!code` or `!summarize`
will be sent to an LLM. The `ModelSelector` decides whether to use a local
Ollama model or AWS Bedrock.

The same features are available over HTTP:

```bash
uvicorn jarvis.api.main:app --reload
```

Use `/tasks/create` and `/tasks/{id}` endpoints to drive the assistant.
