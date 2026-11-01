"""
Smart Feedback Portal — Users Router
======================================
Endpoints:
  GET  /api/v1/users           → List all users  (admin-only in Phase 4)
  GET  /api/v1/users/{id}      → Get user by ID  (admin or own profile in Phase 4)

Auth guards are stubs in Phase 3. Phase 4 will enforce:
  - GET /users        → require_admin
  - GET /users/{id}   → get_current_user + ownership or admin check
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_admin
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=List[UserOut],
    summary="List all users",
    description="Returns all registered users. "
                "**Admin only** (enforced in Phase 4).",
)
def list_users(
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),   # stub — enforced in Phase 4
):
    """
    Return all users ordered by creation date (newest first).
    Passwords are never included — UserOut excludes password_hash.
    """
    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )
    return users


@router.get(
    "/{user_id}",
    response_model=UserOut,
    summary="Get a user by ID",
    description="Returns a single user's profile. "
                "**Admin or own profile only** (enforced in Phase 4).",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),   # stub — enforced in Phase 4
):
    """Return a single user. Raises 404 if not found."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found.",
        )
    return user

