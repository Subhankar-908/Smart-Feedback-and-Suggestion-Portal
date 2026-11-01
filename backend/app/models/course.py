"""
Smart Feedback Portal — Course ORM Model
=========================================
Maps to the `courses` table in PostgreSQL.
Represents courses offered at the institution.

Table: courses
Columns:
  id          SERIAL PRIMARY KEY
  name        VARCHAR(150) NOT NULL
  department  VARCHAR(100) NOT NULL
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    # ── Primary Key ───────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)

    # ── Course Info ───────────────────────────────────────────────
    name = Column(String(150), nullable=False)
    department = Column(String(100), nullable=False, index=True)

    # ── Relationships ─────────────────────────────────────────────
    # A course can appear in many feedback entries.
    feedbacks = relationship("Feedback", back_populates="course")

    def __repr__(self) -> str:
        return f"<Course id={self.id} name={self.name!r} dept={self.department!r}>"

