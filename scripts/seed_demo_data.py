from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.core.database import Base, SessionLocal, engine
from app.core.roles import UserRole
from app.core.security import hash_password
from app.crud.project import add_member_to_project, create_project
from app.crud.task import create_task
from app.crud.user import create_user, get_user_by_email
from app.models import project as project_model  # noqa: F401
from app.models import task as task_model  # noqa: F401
from app.models import user as user_model  # noqa: F401
from app.models.user import User
from app.schemas.project import ProjectCreate
from app.schemas.task import TaskCreate
from app.schemas.auth import UserCreate


def get_or_create_user(db, name: str, email: str, password: str, role: UserRole) -> User:
    existing = get_user_by_email(db, email)
    if existing is not None:
        return existing
    user_in = UserCreate(name=name, email=email, password=password)
    return create_user(db, user_in, role=role)


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = get_or_create_user(
            db,
            name="Admin User",
            email="admin@example.com",
            password="Admin@12345",
            role=UserRole.ADMIN,
        )
        member_one = get_or_create_user(
            db,
            name="Ava Patel",
            email="ava@example.com",
            password="Member@12345",
            role=UserRole.MEMBER,
        )
        member_two = get_or_create_user(
            db,
            name="Noah Kim",
            email="noah@example.com",
            password="Member@12345",
            role=UserRole.MEMBER,
        )

        project_a = db.scalar(select(project_model.Project).where(project_model.Project.name == "Website Redesign"))
        if project_a is None:
            project_a = create_project(
                db,
                creator=admin,
                project_in=ProjectCreate(
                    name="Website Redesign",
                    description="Refresh the public site, improve layout consistency, and update content.",
                    team_member_ids=[member_one.id, member_two.id],
                ),
                team_members=[member_one, member_two],
            )
        else:
            add_member_to_project(db, project_a, member_one)
            add_member_to_project(db, project_a, member_two)

        project_b = db.scalar(select(project_model.Project).where(project_model.Project.name == "Mobile App Launch"))
        if project_b is None:
            project_b = create_project(
                db,
                creator=admin,
                project_in=ProjectCreate(
                    name="Mobile App Launch",
                    description="Prepare app store assets and coordinate the launch checklist.",
                    team_member_ids=[member_one.id],
                ),
                team_members=[member_one],
            )
        else:
            add_member_to_project(db, project_b, member_one)

        task_specs = [
            {
                "title": "Design landing page hero",
                "description": "Create a responsive hero section with updated call-to-action copy.",
                "status": "IN_PROGRESS",
                "assigned_to_id": member_one.id,
                "project_id": project_a.id,
                "due_date": datetime.now(timezone.utc) + timedelta(days=3),
            },
            {
                "title": "Write onboarding copy",
                "description": "Draft concise onboarding steps for new users.",
                "status": "PENDING",
                "assigned_to_id": member_two.id,
                "project_id": project_a.id,
                "due_date": datetime.now(timezone.utc) + timedelta(days=5),
            },
            {
                "title": "Prepare launch checklist",
                "description": "Verify app release assets, release notes, and deployment tasks.",
                "status": "COMPLETED",
                "assigned_to_id": member_one.id,
                "project_id": project_b.id,
                "due_date": datetime.now(timezone.utc) - timedelta(days=1),
            },
        ]

        existing_titles = {row[0] for row in db.execute(select(task_model.Task.title)).all()}
        for task_spec in task_specs:
            if task_spec["title"] in existing_titles:
                continue
            create_task(db, TaskCreate(**task_spec))

        db.commit()
        print("Demo data seeded successfully.")
        print("Admin login: admin@example.com / Admin@12345")
        print("Member login: ava@example.com / Member@12345")
        print("Member login: noah@example.com / Member@12345")
    finally:
        db.close()


if __name__ == "__main__":
    main()
