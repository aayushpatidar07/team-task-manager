import logging
import time
from collections.abc import Generator

from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.pool import NullPool

from app.core.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


# Get database URL
db_url = settings.sqlalchemy_database_url
logger.info(f"DATABASE_URL detected: {bool(settings.database_url)}")
logger.info(f"SQLAlchemy URL (first 80 chars): {db_url[:80]}...")

# Use NullPool for Railway (no connection pooling)
pool_class = NullPool if settings.database_url else None
logger.info(f"Using {'NullPool (Railway)' if pool_class else 'Standard pool (local development)'}")

# Initialize database engine
try:
    if pool_class:
        engine = create_engine(db_url, poolclass=pool_class, future=True, echo=False)
    else:
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=10,
            max_overflow=20,
            future=True,
            echo=False,
        )
    logger.info("✓ Engine created")
except Exception as e:
    logger.error(f"Engine creation failed: {str(e)}")
    engine = None

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
) if engine else None


def test_database_connection() -> bool:
    """Test database connectivity. Returns True if successful."""
    if not engine:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✓ Database connection successful")
        return True
    except OperationalError as e:
        logger.error(f"✗ Connection failed: {str(e)[:100]}")
        return False
    except SQLAlchemyError as e:
        logger.error(f"✗ Database error: {str(e)[:100]}")
        return False
    except Exception as e:
        logger.error(f"✗ Error: {str(e)[:100]}")
        return False


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    if not SessionLocal:
        raise RuntimeError("Database not initialized")
    db = SessionLocal()
    try:
        yield db
    finally:
        try:
            db.close()
        except Exception:
            pass
