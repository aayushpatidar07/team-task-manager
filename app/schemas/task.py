from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.statuses import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=5000)
    status: TaskStatus = TaskStatus.PENDING
    assigned_to_id: int | None = None
    project_id: int | None = None
    due_date: datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=5000)
    status: TaskStatus | None = None
    assigned_to_id: int | None = None
    project_id: int | None = None
    due_date: datetime | None = None


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assigned_to_id: int | None
    project_id: int | None
    created_at: datetime
    updated_at: datetime


class DashboardStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
