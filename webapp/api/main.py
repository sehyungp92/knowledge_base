"""FastAPI application — serves the knowledge base web UI API."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from reading_app.config import Config
from reading_app.db import init_pool, close_pool

from webapp.api.routers.landscape import router as landscape_router
from webapp.api.routers.search import router as search_router
from webapp.api.routers.library import router as library_router
from webapp.api.routers.beliefs import router as beliefs_router
from webapp.api.routers.predictions import router as predictions_router
from webapp.api.routers.graph import router as graph_router
from webapp.api.routers.activity import router as activity_router
from webapp.api.routers.notifications import router as notifications_router
from webapp.api.routers.actions import router as actions_router
from webapp.api.routers.reports import router as reports_router
from webapp.api.routers.concepts import router as concepts_router

config = Config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB pool on startup, close on shutdown."""
    init_pool(config.postgres_dsn)
    yield
    close_pool()


app = FastAPI(
    title="Knowledge Base API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.web_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|\[::1\])(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(landscape_router)
app.include_router(search_router)
app.include_router(library_router)
app.include_router(beliefs_router)
app.include_router(predictions_router)
app.include_router(graph_router)
app.include_router(activity_router)
app.include_router(notifications_router)
app.include_router(actions_router)
app.include_router(reports_router)
app.include_router(concepts_router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
