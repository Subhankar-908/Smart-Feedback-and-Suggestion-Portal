"""
Smart Feedback Portal — Feedback Router
=========================================
Endpoints:
  POST /api/v1/feedback          → Submit feedback  (student, auth in Phase 4; NLP in Phase 9)
  GET  /api/v1/feedback          → List feedback    (admin, with filters; auth in Phase 4)
  GET  /api/v1/feedback/{id}     → Feedback detail  (auth in Phase 4)

Phase 3 behaviour:
  - Feedback is stored with NLP fields as NULL (populated by ML pipeline in Phase 9).
  - user_id is hard-coded to 1 (first seeded user) as a placeholder until
    Phase 4 provides get_current_user with a real JWT-derived user.
  - Anonymous flag is respected: the user field in the response is hidden when True.

Filters supported on GET /feedback:
  ?category=     filter by category  (e.g. "Teaching Pace")
  ?sentiment=    filter by sentiment (Positive / Neutral / Negative)
  ?urgent=       filter by urgency   (true / false)
  ?limit=        max results (default 50, max 200)
  ?offset=       pagination offset   (default 0)
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.dependencies import get_db, get_current_user
from app.models.feedback import Feedback, CATEGORIES, SENTIMENT_LABELS
from app.models.user import User
from app.schemas.feedback import FeedbackCreate, FeedbackOut, FeedbackSummary

router = APIRouter(prefix="/feedback", tags=["Feedback"])


# ── POST /feedback ────────────────────────────────────────────────

@router.post(
    "",
    response_model=FeedbackOut,
    status_code=status.HTTP_201_CREATED,
    summary="Submit feedback",
    description="Submit a new piece of feedback. "
                "NLP analysis (sentiment, category, urgency) is performed "
                "asynchronously — these fields will be `null` initially "
                "and updated once the ML pipeline processes the entry. "
                "**Requires authentication** (enforced in Phase 4).",
)
def create_feedback(
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),   # stub — real user in Phase 4
):
    """
    Create a new feedback record.

    Phase 3 placeholder:
      - user_id defaults to 1 (first seeded user) until auth is wired (Phase 4).
      - NLP fields are NULL; the ML pipeline will populate them (Phase 9).
    """
    # TODO Phase 4: replace with current_user.id once JWT auth is live
    user_id = 1  # placeholder

    # Validate course_id and faculty_id if provided
    if payload.course_id is not None:
        from app.models.course import Course
        if not db.query(Course).filter(Course.id == payload.course_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with id={payload.course_id} not found.",
            )

    if payload.faculty_id is not None:
        from app.models.faculty import Faculty
        if not db.query(Faculty).filter(Faculty.id == payload.faculty_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Faculty with id={payload.faculty_id} not found.",
            )

    feedback = Feedback(
        user_id=user_id,
        course_id=payload.course_id,
        faculty_id=payload.faculty_id,
        feedback_text=payload.feedback_text,
        anonymous=payload.anonymous,
        # NLP fields left NULL — populated by ML pipeline in Phase 9
        sentiment_score=None,
        sentiment_label=None,
        category=None,
        urgent=False,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    # Load relationships so FeedbackOut can include nested objects
    db.refresh(feedback)
    feedback_out = _load_feedback(feedback.id, db)
    return feedback_out


# ── GET /feedback ─────────────────────────────────────────────────

@router.get(
    "",
    response_model=List[FeedbackSummary],
    summary="List feedback",
    description="Returns a paginated, filterable list of all feedback entries. "
                "Supports filtering by category, sentiment label, and urgency. "
                "**Admin only** (enforced in Phase 4).",
)
def list_feedback(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),                              # stub
    category: Optional[str] = Query(
        default=None,
        description=f"Filter by category. One of: {', '.join(CATEGORIES)}",
    ),
    sentiment: Optional[str] = Query(
        default=None,
        description=f"Filter by sentiment. One of: {', '.join(SENTIMENT_LABELS)}",
    ),
    urgent: Optional[bool] = Query(
        default=None,
        description="Filter by urgency flag (true / false).",
    ),
    limit: int = Query(default=50, ge=1, le=200, description="Max results to return."),
    offset: int = Query(default=0, ge=0, description="Pagination offset."),
):
    """
    Return feedback entries with optional filters applied.
    Results are ordered newest-first.
    """
    query = db.query(Feedback)

    # ── Apply filters ─────────────────────────────────────────────
    if category is not None:
        if category not in CATEGORIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid category '{category}'. "
                       f"Must be one of: {', '.join(CATEGORIES)}",
            )
        query = query.filter(Feedback.category == category)

    if sentiment is not None:
        if sentiment not in SENTIMENT_LABELS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sentiment '{sentiment}'. "
                       f"Must be one of: {', '.join(SENTIMENT_LABELS)}",
            )
        query = query.filter(Feedback.sentiment_label == sentiment)

    if urgent is not None:
        query = query.filter(Feedback.urgent == urgent)

    feedback_list = (
        query
        .order_by(Feedback.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return feedback_list


# ── GET /feedback/{id} ────────────────────────────────────────────

@router.get(
    "/{feedback_id}",
    response_model=FeedbackOut,
    summary="Get feedback by ID",
    description="Returns full detail for a single feedback entry, "
                "including nested user, course, and faculty objects. "
                "**Authentication required** (enforced in Phase 4). "
                "The `user` field is `null` for anonymous submissions.",
)
def get_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),   # stub
):
    """Return a single feedback record with all nested relations loaded."""
    feedback = _load_feedback(feedback_id, db)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feedback with id={feedback_id} not found.",
        )
    return feedback


# ── Helper ────────────────────────────────────────────────────────

def _load_feedback(feedback_id: int, db: Session) -> Optional[Feedback]:
    """
    Load a feedback record with user, course, and faculty eagerly joined.
    Hides the user relationship for anonymous submissions before returning.
    """
    feedback = (
        db.query(Feedback)
        .options(
            joinedload(Feedback.user),
            joinedload(Feedback.course),
            joinedload(Feedback.faculty),
        )
        .filter(Feedback.id == feedback_id)
        .first()
    )
    if feedback and feedback.anonymous:
        # Mask the user for anonymous feedback so it doesn't leak in the response
        feedback.user = None
    return feedback

