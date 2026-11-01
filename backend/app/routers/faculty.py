"""
Smart Feedback Portal — Faculty Router
=======================================
Endpoints:
  GET  /api/v1/faculty           → List all faculty members (public)
  GET  /api/v1/faculty/{id}      → Get a single faculty member by ID (public)

Faculty are read-only through the API. They are managed via the
database seed script (database/seed_helper.py).
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.faculty import Faculty
from app.schemas.faculty import FacultyOut

router = APIRouter(prefix="/faculty", tags=["Faculty"])


@router.get(
    "",
    response_model=List[FacultyOut],
    summary="List all faculty members",
    description="Returns all faculty members ordered by department then name. "
                "Used by the feedback form to populate the faculty dropdown.",
)
def list_faculty(db: Session = Depends(get_db)):
    """Return all faculty ordered by department then name."""
    faculty = (
        db.query(Faculty)
        .order_by(Faculty.department, Faculty.name)
        .all()
    )
    return faculty


@router.get(
    "/{faculty_id}",
    response_model=FacultyOut,
    summary="Get a faculty member by ID",
)
def get_faculty_member(faculty_id: int, db: Session = Depends(get_db)):
    """Return a single faculty member. Raises 404 if not found."""
    member = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Faculty member with id={faculty_id} not found.",
        )
    return member

