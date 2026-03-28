from pydantic import BaseModel
from datetime import datetime
from typing import Literal
from app.schemas.label import LabelOut
from app.schemas.assignee import AssigneeOut


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: Literal["todo", "in_progress", "in_review", "done"] = "todo"
    priority: Literal["low", "medium", "high", "critical"] = "medium"
    task_order: int = 0
    duedate: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Literal["todo", "in_progress", "in_review", "done"] | None = None
    priority: Literal["low", "medium", "high", "critical"] | None = None
    task_order: int | None = None
    duedate: datetime | None = None


class TaskLabelInfo(BaseModel):
    label: LabelOut
    model_config = {"from_attributes": True}


class TaskAssigneeInfo(BaseModel):
    assignee: AssigneeOut
    model_config = {"from_attributes": True}


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    task_order: int
    duedate: datetime | None
    created_at: datetime
    updated_at: datetime
    labels: list[TaskLabelInfo] = []
    assignees: list[TaskAssigneeInfo] = []

    model_config = {"from_attributes": True}