from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles
from app.core.roles import UserRole
from app.crud.project import add_member_to_project, create_project, get_project, list_projects, remove_member_from_project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectMemberChange, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["Projects"])


def _project_to_read(project) -> ProjectRead:
    return ProjectRead(
        id=project.id,
        name=project.name,
        description=project.description,
        created_by_id=project.created_by_id,
        created_at=project.created_at,
        team_member_ids=[member.id for member in project.team_members],
    )


@router.get("", response_model=list[ProjectRead])
def read_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
) -> list[ProjectRead]:
    return [_project_to_read(project) for project in list_projects(db)]


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_new_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
) -> ProjectRead:
    team_members: list[User] = []
    for user_id in project_in.team_member_ids:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team member {user_id} not found")
        team_members.append(user)
    project = create_project(db, current_user, project_in, team_members)
    return _project_to_read(project)


@router.post("/{project_id}/members", response_model=ProjectRead)
def add_team_member(
    project_id: int,
    member_in: ProjectMemberChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
) -> ProjectRead:
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    user = db.query(User).filter(User.id == member_in.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _project_to_read(add_member_to_project(db, project, user))


@router.get("/{project_id}", response_model=ProjectRead)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
) -> ProjectRead:
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return _project_to_read(project)


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
) -> ProjectRead:
    from app.crud.project import update_project as update_db_project
    
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    updated = update_db_project(db, project, project_in)
    return _project_to_read(updated)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
) -> None:
    from app.crud.project import delete_project as delete_db_project
    
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    delete_db_project(db, project)


@router.delete("/{project_id}/members/{user_id}", response_model=ProjectRead)
def remove_team_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
) -> ProjectRead:
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _project_to_read(remove_member_from_project(db, project, user))
