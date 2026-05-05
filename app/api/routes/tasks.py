from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user, require_roles
from app.core.roles import UserRole
from app.crud.task import (
    create_task as create_db_task,
    delete_user_task,
    get_dashboard_stats,
    get_task,
    get_user_dashboard_stats,
    get_user_task,
    list_all_tasks,
    list_user_tasks,
    update_user_task,
)
from app.models.user import User
from app.schemas.task import DashboardStats, TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DashboardStats:
    if current_user.role == UserRole.ADMIN:
        stats = get_dashboard_stats(db)
    else:
        stats = get_user_dashboard_stats(db, current_user.id)
    return DashboardStats(**stats)


@router.get("", response_model=list[TaskRead])
def read_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[TaskRead]:
    tasks = list_all_tasks(db) if current_user.role == UserRole.ADMIN else list_user_tasks(db, current_user.id)
    return [TaskRead.model_validate(task) for task in tasks]


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
) -> TaskRead:
    task = create_db_task(db, task_in)
    return TaskRead.model_validate(task)


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> TaskRead:
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if current_user.role != UserRole.ADMIN and task.assigned_to_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return TaskRead.model_validate(task)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> TaskRead:
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if current_user.role != UserRole.ADMIN:
        if task.assigned_to_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update assigned tasks")

        allowed_updates = {"status"}
        incoming_fields = set(task_in.model_dump(exclude_unset=True).keys())
        if incoming_fields - allowed_updates:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Members can only update task status")

    updated_task = update_user_task(db, task, task_in)
    return TaskRead.model_validate(updated_task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
) -> None:
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    delete_user_task(db, task)
