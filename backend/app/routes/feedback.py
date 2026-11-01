"""
routes/feedback.py
==================
Student feedback endpoints:

  GET  /api/feedback/departments  — List distinct departments (for dropdown)
  GET  /api/feedback/courses      — List courses (optional: ?department=...)
  GET  /api/feedback/faculty      — List faculty  (optional: ?department=...)
  POST /api/feedback              — Submit new feedback (students only)
  GET  /api/feedback/my           — Get the current student's feedback history
  GET  /api/feedback/{id}         — Get a specific feedback entry by ID
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from app.models import Course, Faculty, Feedback
from app.models.user import User
from app.schemas.feedback import (
    CourseResponse,
    FacultyResponse,
    FeedbackCreate,
    FeedbackListItem,
    FeedbackResponse,
)
from app.services.auth_service import get_current_student, get_current_user
from app.services.feedback_service import (
    create_feedback,
    get_feedback_by_id,
    get_my_feedback,
)

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])


# ─────────────────────────────────────────────────────────────────
# GET /api/feedback/departments
# ─────────────────────────────────────────────────────────────────
@router.get(
    "/departments",
    response_model=List[str],
    summary="Get list of departments",
)
def get_departments(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Returns a distinct list of department names derived from the courses table.
    Used to populate the Department dropdown on the feedback form.
    """
    rows = db.query(Course.department).distinct().order_by(Course.department).all()
    return [row[0] for row in rows]


# ─────────────────────────────────────────────────────────────────
# GET /api/feedback/courses
# ─────────────────────────────────────────────────────────────────
@router.get(
    "/courses",
    response_model=List[CourseResponse],
    summary="Get courses (optionally filtered by department)",
)
def get_courses(
    department: Optional[str] = Query(None, description="Filter by department name"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Returns courses. If `department` query param is provided, filters to that department.
    Used to populate the Course dropdown on the feedback form.
    """
    query = db.query(Course)
    if department:
        query = query.filter(Course.department == department)
    return query.order_by(Course.name).all()


# ─────────────────────────────────────────────────────────────────
# GET /api/feedback/faculty
# ─────────────────────────────────────────────────────────────────
@router.get(
    "/faculty",
    response_model=List[FacultyResponse],
    summary="Get faculty members (optionally filtered by department)",
)
def get_faculty(
    department: Optional[str] = Query(None, description="Filter by department name"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Returns faculty members. If `department` query param is provided, filters to that department.
    Used to populate the Faculty dropdown on the feedback form.
    """
    query = db.query(Faculty)
    if department:
        query = query.filter(Faculty.department == department)
    return query.order_by(Faculty.name).all()


# ─────────────────────────────────────────────────────────────────
# POST /api/feedback
# ─────────────────────────────────────────────────────────────────
@router.post(
    "",
    response_model=FeedbackResponse,
    status_code=201,
    include_in_schema=False,
)
@router.post(
    "/",
    response_model=FeedbackResponse,
    status_code=201,
    summary="Submit new feedback (students only)",
)
def submit_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student),
):
    """
    Accepts a feedback submission from a student.

    The NLP pipeline (added in Phase 9) will analyze the text and
    populate sentiment_score, sentiment_label, category, and urgent.

    Until Phase 9, those fields will be None/False (analysis pending).
    """
    # ── NLP Pipeline Integration (Phase 9) ───────────────────────
    from ml.pipeline import analyze_feedback
    nlp_result = analyze_feedback(data.feedback_text)
    # ─────────────────────────────────────────────────────────────

    return create_feedback(db, data, current_user, nlp_result)


# ─────────────────────────────────────────────────────────────────
# GET /api/feedback/my
# ─────────────────────────────────────────────────────────────────
@router.get(
    "/my",
    response_model=List[FeedbackListItem],
    summary="Get the current student's feedback history",
)
def my_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student),
):
    """
    Returns all feedback submitted by the currently authenticated student,
    ordered from newest to oldest.
    """
    return get_my_feedback(db, current_user.id)


# ─────────────────────────────────────────────────────────────────
# GET /api/feedback/{feedback_id}
# ─────────────────────────────────────────────────────────────────
@router.get(
    "/{feedback_id}",
    response_model=FeedbackResponse,
    summary="Get a specific feedback entry by ID",
)
def get_single_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns a single feedback entry.
    - Students can only view their own submissions.
    - Admins can view any submission.
    """
    return get_feedback_by_id(db, feedback_id, current_user)
