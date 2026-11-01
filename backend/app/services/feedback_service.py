"""
services/feedback_service.py
=============================
Business logic for creating and retrieving feedback.

Keeping this separate from routes makes it easy to test in isolation
and swap the NLP integration without touching route code.
"""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Course, Faculty, Feedback
from app.models.user import User
from app.schemas.feedback import FeedbackCreate


# ─────────────────────────────────────────────────────────────────
# Helpers to build serializable response dicts
# ─────────────────────────────────────────────────────────────────
def _feedback_to_response(feedback: Feedback, student: User) -> dict:
    """Builds a FeedbackResponse-compatible dict from a Feedback ORM object."""
    return {
        "id":              feedback.id,
        "course_id":       feedback.course_id,
        "faculty_id":      feedback.faculty_id,
        "feedback_text":   feedback.feedback_text,
        "anonymous":       feedback.anonymous,
        "sentiment_score": feedback.sentiment_score,
        "sentiment_label": feedback.sentiment_label,
        "category":        feedback.category,
        "urgent":          feedback.urgent,
        "created_at":      feedback.created_at,
        # Anonymity: hide student name if anonymous = True
        "student_name":    None if feedback.anonymous else student.name,
        "course_name":     feedback.course.name           if feedback.course         else None,
        "faculty_name":    feedback.faculty.name          if feedback.faculty        else None,
        "department":      feedback.course.department     if feedback.course         else None,
    }


def _feedback_to_list_item(feedback: Feedback) -> dict:
    """Builds a FeedbackListItem-compatible dict."""
    return {
        "id":              feedback.id,
        "feedback_text":   feedback.feedback_text,
        "anonymous":       feedback.anonymous,
        "sentiment_label": feedback.sentiment_label,
        "sentiment_score": feedback.sentiment_score,
        "category":        feedback.category,
        "urgent":          feedback.urgent,
        "created_at":      feedback.created_at,
        "course_name":     feedback.course.name           if feedback.course         else None,
        "faculty_name":    feedback.faculty.name          if feedback.faculty        else None,
        "department":      feedback.course.department     if feedback.course         else None,
    }


# ─────────────────────────────────────────────────────────────────
# Create Feedback
# ─────────────────────────────────────────────────────────────────
def create_feedback(
    db: Session,
    data: FeedbackCreate,
    current_user: User,
    nlp_result: dict,
) -> dict:
    """
    Saves a feedback entry to the database with the NLP analysis result.

    Parameters
    ----------
    db           : Database session
    data         : Validated request body (FeedbackCreate)
    current_user : The authenticated student submitting feedback
    nlp_result   : Dict with keys: sentiment_score, sentiment_label,
                   category, urgent — provided by the NLP pipeline
    """
    # Validate course if provided
    course = None
    if data.course_id is not None:
        course = db.query(Course).filter(Course.id == data.course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with id={data.course_id} not found.",
            )

    # Validate faculty if provided
    faculty = None
    if data.faculty_id is not None:
        faculty = db.query(Faculty).filter(Faculty.id == data.faculty_id).first()
        if not faculty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Faculty with id={data.faculty_id} not found.",
            )

    # Determine final category: use user-selected category if provided, otherwise use NLP classified category
    final_category = (
        data.category.strip()
        if (data.category and data.category.strip() and data.category != "Auto-Detect")
        else nlp_result.get("category", "Other")
    )

    feedback = Feedback(
        user_id=current_user.id,
        course_id=data.course_id,
        faculty_id=data.faculty_id,
        feedback_text=data.feedback_text,
        anonymous=data.anonymous,
        sentiment_score=nlp_result.get("sentiment_score"),
        sentiment_label=nlp_result.get("sentiment_label"),
        category=final_category,
        urgent=nlp_result.get("urgent", False),
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return _feedback_to_response(feedback, current_user)


# ─────────────────────────────────────────────────────────────────
# Get Student's Own Feedback
# ─────────────────────────────────────────────────────────────────
def get_my_feedback(db: Session, user_id: int) -> list:
    """Returns all feedback submitted by a specific student, newest first."""
    feedbacks = (
        db.query(Feedback)
        .filter(Feedback.user_id == user_id)
        .order_by(Feedback.created_at.desc())
        .all()
    )
    return [_feedback_to_list_item(f) for f in feedbacks]


# ─────────────────────────────────────────────────────────────────
# Get Single Feedback by ID
# ─────────────────────────────────────────────────────────────────
def get_feedback_by_id(db: Session, feedback_id: int, requesting_user: User) -> dict:
    """
    Returns a single feedback entry.
    - Students may only view their own submissions.
    - Admins may view any submission.
    """
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found.",
        )

    if requesting_user.role == "student" and feedback.user_id != requesting_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this feedback.",
        )

    return _feedback_to_response(feedback, feedback.user)
