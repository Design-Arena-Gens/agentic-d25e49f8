from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import Base, engine
from .routers import auth as auth_router
from .routers import agents as agents_router
from .routers import experiments as experiments_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.backend_cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix=settings.api_v1_prefix)
app.include_router(agents_router.router, prefix=settings.api_v1_prefix)
app.include_router(experiments_router.router, prefix=settings.api_v1_prefix)

@app.get("/")
def read_root():
    return {"name": settings.app_name, "status": "ok"}
