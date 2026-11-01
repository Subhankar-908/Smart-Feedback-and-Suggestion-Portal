"""
database.py
===========
Unified SQLAlchemy database engine and session re-export for the backend.
"""

from app.database import Base, engine, SessionLocal, get_db

__all__ = ["Base", "engine", "SessionLocal", "get_db"]
