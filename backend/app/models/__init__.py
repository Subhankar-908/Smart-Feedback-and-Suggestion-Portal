"""
Smart Feedback Portal — ORM Models Package
==========================================
Import all models here so SQLAlchemy's metadata is fully populated
when Base.metadata.create_all(engine) is called.
"""

from app.models.user import User
from app.models.course import Course
from app.models.faculty import Faculty
from app.models.feedback import Feedback

__all__ = ["User", "Course", "Faculty", "Feedback"]

