"""FastAPI application entry point for the Task Tracker (Module 1).

Exposes a single /health endpoint. CRUD endpoints and storage are added
in later modules per ADR-001.
"""

from pathlib import Path
from typing import Optional
from datetime import datetime, timezone
from fastapi import HTTPException,FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app import storage
from app.models import TaskCreate, TaskResponse, TaskUpdate, TaskStatus

from app.business_rules import validate_status_transition


app = FastAPI(
    title="Task Tracker API",
    description="Module 1 learning project: FastAPI + Pydantic, JSON file storage.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Liveness check.

    Returns HTTP 200 with the service status and the current UTC timestamp
    in ISO 8601 format, e.g. {"status": "ok", "timestamp": "2026-07-05T12:34:56.789+00:00"}.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/", include_in_schema=False)
def read_frontend() -> FileResponse:
    frontend_path = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
    return FileResponse(frontend_path)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(status: Optional[TaskStatus] = None) -> list[TaskResponse]:
    tasks = storage.get_all_tasks()
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    return tasks


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)

@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing.status, payload.status)

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    if not storage.delete_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")