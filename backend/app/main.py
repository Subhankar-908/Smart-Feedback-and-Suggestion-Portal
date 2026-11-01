"""ASGI entry point. Supports `uvicorn app.main:app --reload` from backend/."""
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.routes import auth, feedback, admin
from app.database import init_and_seed_db
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_and_seed_db()
    yield

app = FastAPI(
    title="Smart Feedback & Suggestion Portal",
    description="Student feedback collection, NLP analysis, and institutional analytics.",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.CORS_ORIGINS.split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(auth.router)
app.include_router(feedback.router)
app.include_router(admin.router)

@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Smart Feedback Portal API is running.", "version": "2.0.0"}

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Smart Feedback Portal API", "docs": "/api/docs", "health": "/api/health"}
