from __future__ import annotations

from datetime import date, datetime, timedelta
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator



class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def _validate_title(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("title must not be blank")
    if len(stripped) > 200:
        raise ValueError("title must be at most 200 characters")
    return stripped


def _validate_tags(value: list[str] | None) -> list[str] | None:
    if value is None:
        return None

    normalized_tags: list[str] = []
    seen_tags: set[str] = set()

    for item in value:
        if not isinstance(item, str):
            raise ValueError("tags must contain only strings")

        stripped_tag = item.strip()
        if not stripped_tag:
            raise ValueError("tags must not contain blank values")
        
        if len(stripped_tag) > 30:
            raise ValueError("tags must be at most 30 characters")

        normalized_key = stripped_tag.casefold()
        if normalized_key in seen_tags:
            continue

        seen_tags.add(normalized_key)
        normalized_tags.append(stripped_tag)

    if len(normalized_tags) > 10:
        raise ValueError("tags must be at most 10 values")

    return normalized_tags


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: date | None = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def _check_title(cls, value: str) -> str:
        return _validate_title(value)

    @field_validator("due_date")
    @classmethod
    def _check_due_date(cls, value: date | None) -> date | None:
        if value is None:
            return value
        if isinstance(value, datetime):
            raise ValueError("due_date must be a date in YYYY-MM-DD format")
        if value < date.today() - timedelta(days=365):
            raise ValueError("due_date cannot be more than 365 days in the past")
        return value

    @field_validator("tags")
    @classmethod
    def _check_tags(cls, value: list[str]) -> list[str]:
        return _validate_tags(value) or []


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: date | None = None
    tags: list[str] | None = None

    @field_validator("title")
    @classmethod
    def _check_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return _validate_title(value)

    @field_validator("due_date")
    @classmethod
    def _check_due_date(cls, value: date | None) -> date | None:
        if value is None:
            return value
        if isinstance(value, datetime):
            raise ValueError("due_date must be a date in YYYY-MM-DD format")
        if value < date.today() - timedelta(days=365):
            raise ValueError("due_date cannot be more than 365 days in the past")
        return value

    @field_validator("tags")
    @classmethod
    def _check_tags(cls, value: list[str] | None) -> list[str] | None:
        return _validate_tags(value)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: date | None = None
    tags: list[str] = Field(default_factory=list)
    is_overdue: bool = False
    created_at: datetime
    updated_at: datetime


class TaskStorageRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: date | None = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
