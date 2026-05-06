import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes.auth import router as auth_router
from app.api.routes.projects import router as projects_router
from app.api.routes.tasks import router as tasks_router
from app import models as app_models  # noqa: F401
from app.core.config import settings
from app.core.database import Base, engine, test_database_connection
from app.crud.user import bootstrap_admin_user

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
INDEX_FILE = STATIC_DIR / "index.html"


class SecurityHeadersMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                headers.setdefault(b"x-content-type-options", b"nosniff")
                headers.setdefault(b"x-frame-options", b"DENY")
                headers.setdefault(b"referrer-policy", b"strict-origin-when-cross-origin")
                headers.setdefault(b"permissions-policy", b"camera=(), microphone=(), geolocation=()")
                message["headers"] = list(headers.items())
            await send(message)

        await self.app(scope, receive, send_wrapper)


app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(projects_router, prefix=settings.api_v1_prefix)
app.include_router(tasks_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
def on_startup() -> None:
    """Initialize database and create tables on startup"""
    try:
        logger.info("=" * 60)
        logger.info("STARTUP: Initializing application...")
        logger.info("=" * 60)
        
        db_url_display = settings.sqlalchemy_database_url[:60] + "..."
        logger.info(f"DATABASE_URL: {db_url_display}")
        
        # Test database connection
        logger.info("Connecting to database...")
        if not test_database_connection():
            error_msg = (
                "Cannot connect to database. Check:\n"
                "  1. DATABASE_URL environment variable is set on Railway\n"
                "  2. MySQL service is added to Railway project\n"
                "  3. Local development: ensure MySQL server is running"
            )
            logger.error(error_msg)
            raise RuntimeError("Database connection failed")
        
        # Create tables
        if settings.create_tables_on_startup:
            logger.info("Creating database tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("✓ Database tables created/verified")
        
        # Bootstrap admin user if configured
        if settings.admin_name and settings.admin_email and settings.admin_password:
            from app.core.database import SessionLocal
            db = SessionLocal()
            try:
                bootstrap_admin_user(db, settings.admin_name, settings.admin_email, settings.admin_password)
                logger.info(f"✓ Admin user created: {settings.admin_email}")
            except Exception as e:
                logger.warning(f"Admin bootstrap: {str(e)} (may already exist)")
            finally:
                db.close()
        
        logger.info("=" * 60)
        logger.info("✓ APPLICATION READY")
        logger.info("=" * 60)
        
    except RuntimeError as e:
        logger.error(f"✗ STARTUP FAILED: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"✗ STARTUP ERROR: {str(e)}")
        raise


@app.get("/")
def serve_home() -> FileResponse:
    return FileResponse(INDEX_FILE)


@app.get("/healthz")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(RequestValidationError)
def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.exception_handler(SQLAlchemyError)
def sqlalchemy_exception_handler(_: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": "A database error occurred"})
