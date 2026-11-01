"""
schemas/user.py
===============
Pydantic models for user-related request and response data.

- UserRegister : Body for POST /api/auth/register
- UserLogin    : Body for POST /api/auth/login
- UserResponse : Safe user data returned in responses (no password)
- Token        : JWT token + user data returned after login/register
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    name:       str      = Field(..., min_length=2, max_length=100)
    email:      EmailStr
    password:   str      = Field(..., min_length=6, max_length=128)
    student_id: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=100)
    semester:   Optional[int] = Field(None, ge=1, le=8)


class UserLogin(BaseModel):
    email:    EmailStr
    password: str


class UserResponse(BaseModel):
    id:         int
    name:       str
    email:      str
    student_id: Optional[str]
    department: Optional[str]
    semester:   Optional[int]
    role:       str
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    user:         UserResponse
