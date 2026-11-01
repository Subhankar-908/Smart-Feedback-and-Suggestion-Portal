"""
Smart Feedback Portal — Schemas Package
========================================
Pydantic schemas for request validation and response serialization.
"""

from app.schemas.user import UserRegister, UserLogin, UserResponse, Token
from app.schemas.feedback import (
    CourseResponse,
    FacultyResponse,
    FeedbackCreate,
    FeedbackResponse,
    FeedbackListItem,
)

__all__ = [
    "UserRegister",
    "UserLogin",
    "UserResponse",
    "Token",
    "CourseResponse",
    "FacultyResponse",
    "FeedbackCreate",
    "FeedbackResponse",
    "FeedbackListItem",
]
