"""
routes/auth.py
==============
Authentication endpoints:

  POST /api/auth/register  — Create a new student account
  POST /api/auth/login     — Authenticate and receive a JWT token
  GET  /api/auth/me        — Get the current authenticated user's profile
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserResponse, Token
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# ─────────────────────────────────────────────────────────────────
# POST /api/auth/register
# ─────────────────────────────────────────────────────────────────
@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new student account",
)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """
    Creates a new student account.

    - Email must be unique.
    - Student ID must be unique (if provided).
    - Password is hashed with bcrypt before storage.
    - Returns a JWT token immediately so the user is logged in right away.
    """
    # Check email uniqueness
    if db.query(User).filter(User.email == str(data.email).lower()).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address is already registered.",
        )

    # Check student_id uniqueness (if provided)
    if data.student_id:
        if db.query(User).filter(User.student_id == data.student_id).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This student ID is already registered.",
            )

    user = User(
        name=data.name,
        email=str(data.email).lower(),
        student_id=data.student_id.strip() if data.student_id else None,
        password_hash=hash_password(data.password),
        department=data.department,
        semester=data.semester,
        role="student",  # Public registration always creates a student account
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return Token(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


# ─────────────────────────────────────────────────────────────────
# POST /api/auth/login
# ─────────────────────────────────────────────────────────────────
@router.post(
    "/login",
    response_model=Token,
    summary="Login with email and password",
)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates a user (student or admin) with email and password.
    Returns a JWT token on success.
    Raises 401 with a generic message on failure (don't reveal which field is wrong).
    """
    user = db.query(User).filter(User.email == str(data.email).lower()).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    token = create_access_token({"sub": str(user.id)})
    return Token(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


# ─────────────────────────────────────────────────────────────────
# GET /api/auth/me
# ─────────────────────────────────────────────────────────────────
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get the current user's profile",
)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Returns the profile of the currently authenticated user.
    Useful for the frontend to restore user state after a page refresh.
    """
    return current_user
