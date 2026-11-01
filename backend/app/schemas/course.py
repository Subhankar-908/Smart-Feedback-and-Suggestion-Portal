"""
Smart Feedback Portal — Course Pydantic Schemas
================================================
Schemas for course-related API responses.

Courses are read-only from the API perspective — they are managed
via the database seed and are not created/updated through the API.
"""

from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    """Shared course fields."""

    name: str = Field(..., max_length=150, examples=["Database Management System"])
    department: str = Field(..., max_length=100, examples=["Computer Science"])


class CourseOut(CourseBase):
    """API response schema for a course (includes database id)."""

    id: int

    model_config = {"from_attributes": True}

