"""
main.py
=======
FastAPI application entry point.

This file:
  1. Creates the FastAPI app instance.
  2. Configures CORS (Cross-Origin Resource Sharing) for frontend communication.
  3. Registers all API routers (auth, feedback, admin).
  4. Defines the health-check endpoint.

To run the server:
  cd backend
  uvicorn main:app --reload
"""

import os
import sys

# Ensure root folder is in sys.path for ml package imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, feedback, admin
from app.database import init_and_seed_db
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize tables & seed demo data
    # Fail fast if database initialization is broken instead of serving an
    # apparently healthy API that cannot persist feedback.
    init_and_seed_db()
    yield

# ── App instance ─────────────────────────────────────────────────
app = FastAPI(
    title="Smart Feedback & Suggestion Portal",
    description=(
        "REST API for submitting student feedback and analyzing it with NLP. "
        "Provides analytics and actionable insights for administrators."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",       # Swagger UI at /api/docs
    redoc_url="/api/redoc",     # ReDoc UI at /api/redoc
)

# ── CORS ─────────────────────────────────────────────────────────
# Allow the Vite dev server (port 5173) and a production frontend.
# Update VITE_API_URL in frontend/.env to match your deployed backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(feedback.router)
app.include_router(admin.router)


# ── Health Check ─────────────────────────────────────────────────
@app.get("/api/health", tags=["Health"], summary="Server health check")
def health_check():
    """
    Returns a simple OK response.
    Used to verify the server is running before making other requests.
    """
    return {
        "status":  "ok",
        "message": "Smart Feedback Portal API is running.",
        "version": "1.0.0",
    }
