from sqlalchemy.orm import Session
import logging

from app.core.security import hash_password
from app.core.roles import UserRole
from app.models.user import User
from app.schemas.auth import UserCreate

logger = logging.getLogger(__name__)


def get_user_by_name(db: Session, name: str) -> User | None:
    return db.query(User).filter(User.name == name).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.name.asc()).all()


def create_user(db: Session, user_in: UserCreate, role: UserRole = UserRole.MEMBER) -> User:
    try:
        logger.debug(f"Creating user: {user_in.email.lower()}")
        user = User(
            name=user_in.name,
            email=str(user_in.email).lower(),
            hashed_password=hash_password(user_in.password),
            role=role,
        )
        logger.debug(f"User object created: {user.email}")
        db.add(user)
        logger.debug("User added to session")
        db.commit()
        logger.debug(f"User committed: {user.email}")
        db.refresh(user)
        logger.info(f"✓ User created: ID={user.id}, Email={user.email}, Role={user.role}")
        return user
    except Exception as e:
        logger.error(f"Error creating user: {type(e).__name__}: {str(e)}", exc_info=True)
        db.rollback()
        raise


def bootstrap_admin_user(db: Session, name: str, email: str, password: str) -> User:
    user = get_user_by_name(db, name)
    if user:
        return user

    user = get_user_by_email(db, email)
    if user:
        return user

    admin_user = User(
        name=name,
        email=email.lower(),
        hashed_password=hash_password(password),
        role=UserRole.ADMIN,
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    return admin_user
