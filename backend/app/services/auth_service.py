"""
services/auth_service.py
========================
All authentication and authorization logic lives here.

Functions:
  hash_password()      - bcrypt a plain-text password
  verify_password()    - check a plain-text password against a hash
  create_access_token() - sign a JWT with an expiry
  get_current_user()   - FastAPI dependency: decodes JWT → returns User
  get_current_student() - FastAPI dependency: enforces role = 'student'
  get_current_admin()  - FastAPI dependency: enforces role = 'admin'
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User
from database import get_db

# ── Password hashing ──────────────────────────────────────────────
def hash_password(plain: str) -> str:
    """Returns a bcrypt hash of the given plain-text password."""
    pwd_bytes = plain.encode("utf-8")[:72]
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Returns True if the plain-text password matches the stored hash."""
    try:
        pwd_bytes = plain.encode("utf-8")[:72]
        hash_bytes = hashed.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hash_bytes)
    except Exception:
        return False


# ── JWT ───────────────────────────────────────────────────────────
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a signed JWT token.
    The token contains whatever is in `data` plus an expiry timestamp.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload["exp"] = expire
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# OAuth2 scheme — FastAPI reads the token from the Authorization: Bearer header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ── FastAPI Dependencies ──────────────────────────────────────────
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Decodes the JWT and returns the corresponding User from the database.
    Raises 401 if the token is missing, invalid, or the user no longer exists.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except (JWTError, TypeError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_student(current_user: User = Depends(get_current_user)) -> User:
    """Ensures the authenticated user is a student. Raises 403 otherwise."""
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This endpoint is for students only.",
        )
    return current_user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Ensures the authenticated user is an admin. Raises 403 otherwise."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This endpoint is for administrators only.",
        )
    return current_user
