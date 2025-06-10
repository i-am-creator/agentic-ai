from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from ..orchestrator import MultiContextPlanner
from ..model_selector import ModelSelector

app = FastAPI(title="Jarvis API")
planner = MultiContextPlanner()
selector = ModelSelector()

class Task(BaseModel):
    """Represents a task to be executed by the system."""
    description: str
    expected_output: str = Field(default="Analysis and recommendations")  # Added default
    context: Optional[dict] = None


class CreateTaskRequest(BaseModel):
    prompt: str


class CreateTaskResponse(BaseModel):
    task_id: str


class TaskInput(BaseModel):
    content: str


class TaskOutput(BaseModel):
    content: str


class TaskInfo(BaseModel):
    id: str
    prompt: str
    status: str


class ModelSelectionRequest(BaseModel):
    prompt: str


class ModelSelectionResponse(BaseModel):
    model: str


@app.post("/select-model", response_model=ModelSelectionResponse)
def select_model(req: ModelSelectionRequest):
    model = selector.select(req.prompt)
    return ModelSelectionResponse(model=model)



  @app.post("/tasks/create", response_model=CreateTaskResponse)
def create_task(req: CreateTaskRequest):
    task_id = planner.create_task(req.prompt)
    return CreateTaskResponse(task_id=task_id)


@app.get("/tasks", response_model=list[TaskInfo])
def list_tasks(status: str | None = None):
    tasks = planner.context_manager.list_tasks(status=status)
    return [TaskInfo(id=t.id, prompt=t.prompt, status=t.status) for t in tasks]


@app.get("/tasks/{task_id}", response_model=TaskInfo)
def get_task(task_id: str):
    t = planner.context_manager.get_task_record(task_id)
    if t is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskInfo(id=t.id, prompt=t.prompt, status=t.status)


@app.post("/tasks/{task_id}", response_model=TaskOutput)
def handle_task(task_id: str, input: TaskInput):
    try:
        output = planner.handle(task_id, input.content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return TaskOutput(content=output)


@app.post("/tasks/{task_id}/update", response_model=TaskOutput)
def update_task(task_id: str, input: TaskInput):
    """Append new input to an existing task and process it."""
    try:
        output = planner.handle(task_id, input.content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return TaskOutput(content=output)
