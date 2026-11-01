"""
Smart Feedback Portal — Health Router
======================================
GET /api/v1/health

Returns the application status and database connectivity state.
Used by monitoring tools, deployment health checks, and the frontend
to detect if the API is reachable.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.dependencies import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    summary="Health check",
    description="Returns API status and database connectivity. "
                "Safe to call without authentication.",
)
def health_check(db: Session = Depends(get_db)):
    """
    Perform a lightweight liveness check.

    - Runs `SELECT 1` to verify the database connection is alive.
    - Returns `'database': 'error'` (not a 500) if the DB is unreachable,
      so the frontend can show a meaningful message instead of crashing.
    """
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "database": db_status,
        "version": "1.0.0",
    }

