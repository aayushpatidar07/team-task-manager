import logging
from collections.abc import Generator

from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from app.core.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


# Get database URL
db_url = settings.sqlalchemy_database_url

# Initialize database engine with production-safe settings
engine = create_engine(
    db_url,
    pool_pre_ping=True,  # Verify connection before using
    pool_recycle=3600,   # Recycle connections every hour
    pool_size=10,
    max_overflow=20,
    future=True,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


def test_database_connection() -> bool:
    """
    Test database connectivity.
    Returns True if successful, False otherwise.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✓ Database connection successful")
        return True
    except OperationalError as e:
        logger.error(f"✗ Database connection failed - Check DATABASE_URL: {str(e)}")
        return False
    except SQLAlchemyError as e:
        logger.error(f"✗ Database error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"✗ Unexpected error: {str(e)}")
        return False


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    Ensures session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
