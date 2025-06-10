from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ..orchestrator import MultiContextPlanner
from ..model_selector import ModelSelector

app = FastAPI(title="Jarvis API")
planner = MultiContextPlanner()
selector = ModelSelector()

class CreateTaskRequest(BaseModel):
    prompt: str

class CreateTaskResponse(BaseModel):
    task_id: str

class TaskInput(BaseModel):
    content: str

class TaskOutput(BaseModel):
    content: str

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

@app.post("/tasks/{task_id}", response_model=TaskOutput)
def handle_task(task_id: str, input: TaskInput):
    try:
        output = planner.handle(task_id, input.content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return TaskOutput(content=output)
