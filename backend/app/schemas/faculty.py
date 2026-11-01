"""
Smart Feedback Portal — Faculty Pydantic Schemas
=================================================
Schemas for faculty-related API responses.

Faculty are read-only from the API perspective — managed via DB seed.
"""

from pydantic import BaseModel, Field


class FacultyBase(BaseModel):
    """Shared faculty fields."""

    name: str = Field(..., max_length=100, examples=["Dr. Rajesh Kumar"])
    department: str = Field(..., max_length=100, examples=["Computer Science"])


class FacultyOut(FacultyBase):
    """API response schema for a faculty member (includes database id)."""

    id: int

    model_config = {"from_attributes": True}

