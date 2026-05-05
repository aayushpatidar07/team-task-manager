from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


def list_projects(db: Session) -> list[Project]:
    return db.query(Project).order_by(Project.created_at.desc()).all()


def get_project(db: Session, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.id == project_id).first()


def create_project(db: Session, creator: User, project_in: ProjectCreate, team_members: list[User]) -> Project:
    project = Project(
        name=project_in.name,
        description=project_in.description,
        created_by_id=creator.id,
        team_members=team_members,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project: Project, project_in: ProjectUpdate) -> Project:
    updates = project_in.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


def add_member_to_project(db: Session, project: Project, user: User) -> Project:
    if user not in project.team_members:
        project.team_members.append(user)
        db.commit()
        db.refresh(project)
    return project


def remove_member_from_project(db: Session, project: Project, user: User) -> Project:
    if user in project.team_members:
        project.team_members.remove(user)
        db.commit()
        db.refresh(project)
    return project


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()
