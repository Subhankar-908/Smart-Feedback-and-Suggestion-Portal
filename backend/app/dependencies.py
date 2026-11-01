"""
Smart Feedback Portal — Shared FastAPI Dependencies
====================================================
Centralises all injectable dependencies used across routers.

Phase 3: get_db is live. Auth stubs return None — replaced in Phase 4
         with real JWT verification.

Usage in routers:
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from app.dependencies import get_db, get_current_user, require_admin
"""

# FastAPI is provided by the backend environment; suppress editor-only import
# resolution noise when the selected Python interpreter lacks the environment.
from fastapi import Depends  # type: ignore[reportMissingImports]
from sqlalchemy.orm import Session

from app.database import get_db  # re-export so routers only import from here

# ── Database dependency ───────────────────────────────────────────
# Already defined in database.py; re-exported here for convenience.
# Usage:  db: Session = Depends(get_db)
__all__ = ["get_db", "get_current_user", "require_admin"]


# ── Auth dependencies (stubs — replaced in Phase 4) ──────────────

def get_current_user(db: Session = Depends(get_db)):
    """
    STUB — Phase 3 only.

    In Phase 4 this will:
      1. Extract the Bearer token from the Authorization header.
      2. Decode and verify the JWT.
      3. Look up the user in the database.
      4. Raise HTTP 401 if the token is missing or invalid.

    For now it returns None so routes can be tested without auth.
    """
    return None  # replaced in Phase 4


def require_admin(current_user=Depends(get_current_user)):
    """
    STUB — Phase 3 only.

    In Phase 4 this will verify that current_user.role == 'admin'
    and raise HTTP 403 if not.

    For now it passes through so admin routes can be tested without auth.
    """
    # TODO Phase 4: enforce role check
    # if current_user is None or current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Admin access required.")
    return current_user

