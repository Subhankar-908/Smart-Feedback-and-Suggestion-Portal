"""
Smart Feedback Portal — Courses Router
=======================================
Endpoints:
  GET  /api/v1/courses           → List all courses (public)
  GET  /api/v1/courses/{id}      → Get a single course by ID (public)

Courses are read-only through the API. They are managed via the
database seed script (database/seed_helper.py).
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.course import Course
from app.schemas.course import CourseOut

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get(
    "",
    response_model=List[CourseOut],
    summary="List all courses",
    description="Returns all courses available in the system. "
                "Used by the feedback submission form to populate the course dropdown.",
)
def list_courses(db: Session = Depends(get_db)):
    """Return all courses ordered by department then name."""
    courses = (
        db.query(Course)
        .order_by(Course.department, Course.name)
        .all()
    )
    return courses


@router.get(
    "/{course_id}",
    response_model=CourseOut,
    summary="Get a course by ID",
)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Return a single course. Raises 404 if not found."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id={course_id} not found.",
        )
    return course

