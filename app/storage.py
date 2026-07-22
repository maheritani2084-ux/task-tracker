from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskStorageRecord, TaskUpdate

_tasks: dict[str, TaskStorageRecord] = {}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _task_from_record(record: TaskStorageRecord) -> TaskResponse:
    return TaskResponse(**record.model_dump(), is_overdue=compute_is_overdue(record.model_dump()))


def compute_is_overdue(task: dict) -> bool:
    due_date = task.get("due_date")
    status = task.get("status")
    if due_date is None:
        return False
    if isinstance(due_date, str):
        due_date = date.fromisoformat(due_date)
    if status == TaskStatus.DONE:
        return False
    return due_date < date.today()


def add_task(payload: TaskCreate) -> TaskResponse:
    task_id = str(uuid4())
    now = _now()
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = TaskStorageRecord(**task.model_dump(exclude={"is_overdue"}))
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:
    tasks = [_task_from_record(record) for record in _tasks.values()]
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    if priority is not None:
        tasks = [t for t in tasks if t.priority == priority]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    record = _tasks.get(task_id)
    if record is None:
        return None
    return _task_from_record(record)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    record = _tasks.get(task_id)
    if record is None:
        return None
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        return _task_from_record(record)
    updated_data = {**record.model_dump(), **changes, "updated_at": _now()}
    _tasks[task_id] = TaskStorageRecord(**updated_data)
    return _task_from_record(_tasks[task_id])


def delete_task(task_id: str) -> bool:
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False


def _reset() -> None:
    _tasks.clear()