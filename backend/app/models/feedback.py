"""
Smart Feedback Portal — Feedback ORM Model
===========================================
Maps to the `feedback` table in PostgreSQL.
This is the core entity of the application.

Stores:
  - The raw feedback text submitted by a student
  - Foreign keys to user, course, and faculty
  - NLP analysis results (populated by the ML pipeline in Phase 9)

Table: feedback
Columns:
  id               SERIAL PRIMARY KEY
  user_id          INTEGER → users.id  (ON DELETE CASCADE)
  course_id        INTEGER → courses.id (ON DELETE SET NULL)
  faculty_id       INTEGER → faculty.id (ON DELETE SET NULL)
  feedback_text    TEXT NOT NULL
  anonymous        BOOLEAN NOT NULL DEFAULT FALSE

  -- NLP results (NULL until the pipeline processes the submission)
  sentiment_score  FLOAT
  sentiment_label  VARCHAR(10) CHECK IN ('Positive', 'Neutral', 'Negative')
  category         VARCHAR(30) CHECK IN (defined categories)
  urgent           BOOLEAN NOT NULL DEFAULT FALSE

  created_at       TIMESTAMP WITH TIME ZONE DEFAULT NOW()
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base

# ── Allowed values (kept in sync with schema.sql) ────────────────
SENTIMENT_LABELS = ("Positive", "Neutral", "Negative")
CATEGORIES = (
    "Teaching Pace",
    "Lab Facilities",
    "Canteen & Food",
    "Placements & Training",
    "College Services & Admin",
    "Infrastructure & Hostel",
    "Library Services",
    "Syllabus Coverage",
    "Infrastructure",
    "Other",
)


class Feedback(Base):
    __tablename__ = "feedback"

    __table_args__ = (
        CheckConstraint(
            "sentiment_label IN ('Positive', 'Neutral', 'Negative')",
            name="ck_feedback_sentiment_label",
        ),
        CheckConstraint(
            "category IN ("
            "'Teaching Pace', 'Lab Facilities', 'Canteen & Food', 'Placements & Training', "
            "'College Services & Admin', 'Infrastructure & Hostel', 'Library Services', "
            "'Syllabus Coverage', 'Infrastructure', 'Other')",
            name="ck_feedback_category",
        ),
    )

    # ── Primary Key ───────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)

    # ── Foreign Keys ──────────────────────────────────────────────
    # ON DELETE CASCADE: if the user is deleted, their feedback is deleted too
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ON DELETE SET NULL: feedback stays if a course/faculty is removed
    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    faculty_id = Column(
        Integer,
        ForeignKey("faculty.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ── Feedback Content ──────────────────────────────────────────
    feedback_text = Column(Text, nullable=False)
    anonymous = Column(Boolean, nullable=False, default=False, index=True)

    # ── NLP Results (populated by ML pipeline after submission) ───
    # NULL until the NLP pipeline processes this record
    sentiment_score = Column(Float, nullable=True)          # e.g. 0.82 or -0.63
    sentiment_label = Column(String(10), nullable=True, index=True)  # Positive/Neutral/Negative
    category = Column(String(30), nullable=True, index=True)         # e.g. "Teaching Pace"
    urgent = Column(Boolean, nullable=False, default=False, index=True)

    # ── Timestamps ────────────────────────────────────────────────
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    # ── Relationships ─────────────────────────────────────────────
    user = relationship("User", back_populates="feedbacks")
    course = relationship("Course", back_populates="feedbacks")
    faculty = relationship("Faculty", back_populates="feedbacks")

    def __repr__(self) -> str:
        return (
            f"<Feedback id={self.id} user_id={self.user_id} "
            f"label={self.sentiment_label!r} urgent={self.urgent}>"
        )

