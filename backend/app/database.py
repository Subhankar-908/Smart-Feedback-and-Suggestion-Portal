"""
database.py
===========
SQLAlchemy database engine, session configuration, and automatic initialization.

Features:
- Tries connecting to PostgreSQL first.
- Automatically falls back to SQLite if PostgreSQL server is offline on localhost.
- Automatically creates tables and seeds demo accounts & courses if empty.
"""

import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

# Base class for all ORM models
Base = declarative_base()

# Use the configured database exactly as requested. Silently falling back from
# PostgreSQL to SQLite can split production data, so connection failures are
# surfaced and the API fails fast during startup.
db_url = settings.DATABASE_URL
if db_url.startswith("sqlite"):
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    engine = create_engine(db_url, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency yielding a database session per request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_and_seed_db():
    """
    Automatically creates all tables and seeds demo users, courses, faculty, and sample feedback.
    """
    from app.models import User, Course, Faculty, Feedback
    import bcrypt

    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        def _hash(pwd: str) -> str:
            pwd_bytes = pwd.encode("utf-8")[:72]
            return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt(rounds=10)).decode("utf-8")

        # Check if users already seeded
        user_count = db.query(func.count(User.id)).scalar() or 0
        if user_count > 0:
            # Never reset credentials on application restart. Existing accounts
            # and user-managed passwords must remain unchanged. Repair older
            # databases that contain students but no administrator account.
            existing_admin = db.query(User).filter(User.role == "admin").first()
            if existing_admin is None:
                db.add(User(
                    name="Administrator",
                    email=settings.ADMIN_EMAIL,
                    password_hash=_hash(settings.ADMIN_PASSWORD),
                    role="admin",
                ))
                db.commit()
            return

        print("[Database] Initializing data...")

        # 1. Admin Account
        admin = User(
            name="Administrator",
            email=settings.ADMIN_EMAIL,
            password_hash=_hash(settings.ADMIN_PASSWORD),
            role="admin",
        )

        # Demo student accounts are opt-in. Normal installations only create
        # the administrator and reference data; real students self-register.
        students = []
        if settings.SEED_DEMO_DATA:
            students = [
                User(name="Arjun Mehta", email="arjun.mehta@college.edu", student_id="CS2022001",
                     password_hash=_hash("Student@123"), department="Computer Science", semester=6, role="student"),
                User(name="Priya Patel", email="priya.patel@college.edu", student_id="CS2022002",
                     password_hash=_hash("Student@123"), department="Computer Science", semester=6, role="student"),
                User(name="Rohan Gupta", email="rohan.gupta@college.edu", student_id="EC2022015",
                     password_hash=_hash("Student@123"), department="Electronics & Communication", semester=4, role="student"),
            ]

        # 3. Courses
        courses = [
            Course(name="Database Management System", department="Computer Science"),
            Course(name="Operating Systems", department="Computer Science"),
            Course(name="Data Structures & Algorithms", department="Computer Science"),
            Course(name="Computer Networks", department="Computer Science"),
            Course(name="Digital Electronics", department="Electronics & Communication"),
            Course(name="Signals & Systems", department="Electronics & Communication"),
            Course(name="Thermodynamics", department="Mechanical Engineering"),
            Course(name="Structural Analysis", department="Civil Engineering"),
        ]

        # 4. Faculty
        faculty_members = [
            Faculty(name="Dr. Rajesh Kumar", department="Computer Science"),
            Faculty(name="Prof. Sunita Sharma", department="Computer Science"),
            Faculty(name="Dr. Amit Verma", department="Electronics & Communication"),
            Faculty(name="Prof. Manoj Patel", department="Mechanical Engineering"),
            Faculty(name="Dr. Vikram Singh", department="Civil Engineering"),
            Faculty(name="Prof. Ananya Nair", department="Computer Science"),
        ]

        db.add_all([admin] + students + courses + faculty_members)
        db.commit()
        if not settings.SEED_DEMO_DATA:
            print("[Database] Set SEED_DEMO_DATA=true to load optional sample students and feedback.")
            return

        # 5. Sample Initial Feedbacks with NLP Pre-computation
        sample_feedbacks = [
            Feedback(
                user_id=students[0].id,
                course_id=courses[0].id,
                faculty_id=faculty_members[0].id,
                feedback_text="The DBMS lectures are well-structured and Dr. Kumar explains every concept with real-world examples. Really enjoying the course.",
                anonymous=False,
                sentiment_score=0.82,
                sentiment_label="Positive",
                category="Teaching Pace",
                urgent=False,
            ),
            Feedback(
                user_id=students[1].id,
                course_id=courses[0].id,
                faculty_id=faculty_members[0].id,
                feedback_text="Lab computers in the DBMS lab keep crashing. Many systems have been non-functional for over two weeks. This is seriously affecting our practicals.",
                anonymous=True,
                sentiment_score=-0.75,
                sentiment_label="Negative",
                category="Lab Facilities",
                urgent=True,
            ),
            Feedback(
                user_id=students[0].id,
                course_id=courses[1].id,
                faculty_id=faculty_members[1].id,
                feedback_text="Operating Systems class moves a little fast. Some students find it hard to keep up with the pace of lectures.",
                anonymous=False,
                sentiment_score=-0.35,
                sentiment_label="Negative",
                category="Teaching Pace",
                urgent=False,
            ),
            Feedback(
                user_id=students[2].id,
                course_id=courses[4].id,
                faculty_id=faculty_members[2].id,
                feedback_text="Digital Electronics lab equipment is outdated. Oscilloscopes are broken in half the lab. Please replace them urgently.",
                anonymous=True,
                sentiment_score=-0.80,
                sentiment_label="Negative",
                category="Lab Facilities",
                urgent=True,
            ),
            Feedback(
                user_id=students[1].id,
                course_id=courses[2].id,
                faculty_id=faculty_members[5].id,
                feedback_text="DSA practicals are well-planned. The lab machines are fast and all required IDEs are pre-installed.",
                anonymous=False,
                sentiment_score=0.78,
                sentiment_label="Positive",
                category="Lab Facilities",
                urgent=False,
            ),
            Feedback(
                user_id=students[0].id,
                course_id=courses[6].id,
                faculty_id=faculty_members[3].id,
                feedback_text="The classroom used for Thermodynamics has broken ceiling fans. It gets extremely hot during afternoon sessions.",
                anonymous=False,
                sentiment_score=-0.65,
                sentiment_label="Negative",
                category="Infrastructure",
                urgent=True,
            ),
        ]

        if settings.SEED_DEMO_DATA:
            db.add_all(sample_feedbacks)
        db.commit()
        print("[Database] Administrator and reference data initialized.")
        if settings.SEED_DEMO_DATA:
            print("[Database] Optional demo students and feedback initialized.")

    except Exception as e:
        db.rollback()
        print(f"[Database] Initialization failed: {e}")
        raise
    finally:
        db.close()
