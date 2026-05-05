from sqlalchemy.orm import Session

from app.core.statuses import TaskStatus
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate


def list_all_tasks(db: Session) -> list[Task]:
    return db.query(Task).order_by(Task.status.asc(), Task.created_at.desc()).all()


def list_user_tasks(db: Session, user_id: int) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.assigned_to_id == user_id)
        .order_by(Task.status.asc(), Task.created_at.desc())
        .all()
    )


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def get_user_task(db: Session, task_id: int, user_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id, Task.assigned_to_id == user_id).first()


def create_task(db: Session, task_in: TaskCreate) -> Task:
    data = task_in.model_dump()
    data.setdefault("status", TaskStatus.PENDING)
    task = Task(**data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_user_task(db: Session, task: Task, task_in: TaskUpdate) -> Task:
    updates = task_in.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_user_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()


def assign_task(db: Session, task: Task, user: User | None = None, project_id: int | None = None) -> Task:
    if user is not None:
        task.assigned_to_id = user.id
    if project_id is not None:
        task.project_id = project_id
    db.commit()
    db.refresh(task)
    return task


def get_dashboard_stats(db: Session) -> dict[str, int]:
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == TaskStatus.COMPLETED).count()
    pending_tasks = db.query(Task).filter(Task.status == TaskStatus.PENDING).count()
    overdue_tasks = db.query(Task).filter(Task.status == TaskStatus.OVERDUE).count()
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,
    }


def get_user_dashboard_stats(db: Session, user_id: int) -> dict[str, int]:
    total_tasks = db.query(Task).filter(Task.assigned_to_id == user_id).count()
    completed_tasks = db.query(Task).filter(
        Task.assigned_to_id == user_id,
        Task.status == TaskStatus.COMPLETED,
    ).count()
    pending_tasks = db.query(Task).filter(
        Task.assigned_to_id == user_id,
        Task.status == TaskStatus.PENDING,
    ).count()
    overdue_tasks = db.query(Task).filter(
        Task.assigned_to_id == user_id,
        Task.status == TaskStatus.OVERDUE,
    ).count()
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,
    }
