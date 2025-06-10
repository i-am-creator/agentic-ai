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
  * `SummarizerAgent` calls an LLM to condense task history.

## Usage

Create a virtual environment with Python 3.10+ and install the project in
editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the Typer-based CLI with a command. Prefixes select agents:

```bash
jarvis !sh ls
jarvis !file read README.md
jarvis !code path/to/file.py replacement
jarvis !summarize
```

Anything that does not start with `!sh`, `!file`, `!code` or `!summarize`
will be sent to an LLM. The `ModelSelector` decides whether to use a local
Ollama model or AWS Bedrock.

The same features are available over HTTP:

```bash
uvicorn jarvis.api.main:app --reload
```

The API exposes routes to create and manage tasks:

```
POST /tasks/create        -> returns a task_id
GET  /tasks               -> list all tasks (optionally filter by status)
GET  /tasks/{id}          -> retrieve a single task record
POST /tasks/{id}          -> process input for an existing task
POST /tasks/{id}/update   -> alias of the above for clarity
```

The `/tasks/{id}/update` endpoint returns a short summary when you call `!summarize`.

### Task queue

All created tasks are stored with a status flag. Pending tasks can be processed
one by one using the task runner:

```bash
python -m jarvis.task_runner
```
