"""
Smart Feedback Portal — User ORM Model
=======================================
Maps to the `users` table in PostgreSQL.
Stores both student and admin accounts, distinguished by `role`.

Table: users
Columns:
  id            SERIAL PRIMARY KEY
  name          VARCHAR(100) NOT NULL
  email         VARCHAR(150) UNIQUE NOT NULL
  student_id    VARCHAR(20)  UNIQUE  (students only, NULL for admins)
  password_hash VARCHAR(255) NOT NULL
  department    VARCHAR(100)
  semester      INTEGER (1–8, students only)
  role          VARCHAR(10) CHECK IN ('student', 'admin')
  created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
"""

from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    # ── Primary Key ───────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)

    # ── Identity ──────────────────────────────────────────────────
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)

    # Unique student roll number; NULL for admin accounts
    student_id = Column(String(20), unique=True, nullable=True)

    # Bcrypt-hashed password stored as a string
    password_hash = Column(String(255), nullable=False)

    # ── Academic Info (students only) ─────────────────────────────
    department = Column(String(100), nullable=True)
    semester = Column(
        Integer,
        CheckConstraint("semester BETWEEN 1 AND 8", name="ck_users_semester"),
        nullable=True,
    )

    # ── Role ──────────────────────────────────────────────────────
    role = Column(
        String(10),
        CheckConstraint("role IN ('student', 'admin')", name="ck_users_role"),
        nullable=False,
        default="student",
    )

    # ── Timestamps ────────────────────────────────────────────────
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # ── Relationships ─────────────────────────────────────────────
    # One user can submit many feedback entries.
    # cascade="all, delete-orphan" mirrors ON DELETE CASCADE in schema.sql
    feedbacks = relationship(
        "Feedback",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} role={self.role!r}>"

