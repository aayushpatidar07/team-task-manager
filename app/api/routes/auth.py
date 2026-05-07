from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.roles import UserRole
from app.core.security import create_access_token, verify_password
from app.crud.user import create_user, get_user_by_email, list_users
from app.models.user import User
from app.schemas.auth import LoginRequest, Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> Token:
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        email_lower = str(user_in.email).lower()
        existing_user = get_user_by_email(db, email_lower)
        if existing_user:
            logger.info(f"Registration attempt with existing email: {email_lower}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        logger.info(f"Creating user: {email_lower}")
        user = create_user(db, user_in, role=UserRole.MEMBER)
        logger.info(f"User created successfully: {user.id} - {user.email}")
        
        access_token = create_access_token(subject=user.email, extra_claims={"role": user.role.value})
        return Token(access_token=access_token, user=UserRead.model_validate(user))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Registration failed: {str(e)}")


@router.post("/login", response_model=Token)
def login(login_in: LoginRequest, db: Session = Depends(get_db)) -> Token:
    user = get_user_by_email(db, str(login_in.email).lower())
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token(subject=user.email, extra_claims={"role": user.role.value})
    return Token(access_token=access_token, user=UserRead.model_validate(user))


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_active_user)) -> UserRead:
    return UserRead.model_validate(current_user)


@router.get("/users", response_model=list[UserRead])
def list_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[UserRead]:
    # Only admins can list all users
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")
    
    users = list_users(db)
    return [UserRead.model_validate(user) for user in users]
