"""
Smart Feedback Portal — Faculty ORM Model
==========================================
Maps to the `faculty` table in PostgreSQL.
Represents faculty members at the institution.

Table: faculty
Columns:
  id          SERIAL PRIMARY KEY
  name        VARCHAR(100) NOT NULL
  department  VARCHAR(100) NOT NULL
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Faculty(Base):
    __tablename__ = "faculty"

    # ── Primary Key ───────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)

    # ── Faculty Info ──────────────────────────────────────────────
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False, index=True)

    # ── Relationships ─────────────────────────────────────────────
    # A faculty member can be associated with many feedback entries.
    feedbacks = relationship("Feedback", back_populates="faculty")

    def __repr__(self) -> str:
        return f"<Faculty id={self.id} name={self.name!r} dept={self.department!r}>"

