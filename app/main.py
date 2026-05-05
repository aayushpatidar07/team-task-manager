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
from app.core.database import Base, engine
from app.crud.user import bootstrap_admin_user

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
    if settings.create_tables_on_startup:
        Base.metadata.create_all(bind=engine)

    if settings.admin_name and settings.admin_email and settings.admin_password:
        from app.core.database import SessionLocal

        db = SessionLocal()
        try:
            bootstrap_admin_user(db, settings.admin_name, settings.admin_email, settings.admin_password)
        finally:
            db.close()


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
    return JSONResponse(status_code=500, content={"detail": "A database error occurred"})
