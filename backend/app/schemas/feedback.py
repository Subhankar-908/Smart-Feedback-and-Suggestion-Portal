"""
schemas/feedback.py
===================
Pydantic models for feedback, courses, and faculty data.

- CourseResponse    : Course data for dropdown menus
- FacultyResponse   : Faculty data for dropdown menus
- FeedbackCreate    : Request body for POST /api/feedback
- FeedbackResponse  : Full feedback detail response
- FeedbackListItem  : Compact feedback item used in lists
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class CourseResponse(BaseModel):
    id:         int
    name:       str
    department: str

    model_config = {"from_attributes": True}


class FacultyResponse(BaseModel):
    id:         int
    name:       str
    department: str

    model_config = {"from_attributes": True}


class FeedbackCreate(BaseModel):
    course_id:     Optional[int] = None
    faculty_id:    Optional[int] = None
    category:      Optional[str] = None
    feedback_text: str           = Field(..., min_length=10, max_length=2000,
                                         description="The student's feedback text.")
    anonymous:     bool          = False

    @field_validator("feedback_text")
    @classmethod
    def validate_feedback_text(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 10:
            raise ValueError("Feedback must contain at least 10 non-whitespace characters.")
        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: Optional[str]) -> Optional[str]:
        allowed = {
            "Teaching Pace", "Lab Facilities", "Canteen & Food",
            "Placements & Training", "College Services & Admin",
            "Infrastructure & Hostel", "Library Services", "Syllabus Coverage",
            "Infrastructure", "Other", "Auto-Detect",
        }
        if value is not None and value not in allowed:
            raise ValueError("Select a valid feedback category or leave it empty for automatic classification.")
        return value


class FeedbackResponse(BaseModel):
    id:              int
    course_id:       Optional[int]
    faculty_id:      Optional[int]
    feedback_text:   str
    anonymous:       bool
    sentiment_score: Optional[float]
    sentiment_label: Optional[str]
    category:        Optional[str]
    urgent:          bool
    created_at:      datetime

    # Resolved from relationships — not stored as columns
    student_name: Optional[str]   # None if anonymous
    course_name:  Optional[str]
    faculty_name: Optional[str]
    department:   Optional[str]


class FeedbackListItem(BaseModel):
    id:              int
    feedback_text:   str
    anonymous:       bool
    sentiment_label: Optional[str]
    sentiment_score: Optional[float]
    category:        Optional[str]
    urgent:          bool
    created_at:      datetime
    course_name:     Optional[str]
    faculty_name:    Optional[str]
    department:      Optional[str]
