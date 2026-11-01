"""
Smart Feedback Portal — Database Seeder
=======================================
This script seeds the database with realistic demo data.

Why a Python script instead of pure SQL?
  bcrypt password hashes cannot be generated inside SQL.
  This script hashes passwords properly using bcrypt, then inserts all data.

ADMIN CREDENTIALS:
------------------
    Set ADMIN_EMAIL and ADMIN_PASSWORD in the environment before running.
    Demo student credentials are for local testing only.

USAGE:
------
  1. Make sure the schema has been applied:
       psql -d smart_feedback_db -f schema.sql

  2. Set your DATABASE_URL environment variable or update the
     DATABASE_URL constant below.

  3. Run:
       cd database
       pip install psycopg2-binary bcrypt python-dotenv
       python seed_helper.py
"""

import os
import sys
import bcrypt
import psycopg2
from datetime import datetime, timedelta, timezone
import random

# ── Configuration ───────────────────────────────────────────────
# Update this if not using a .env file
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/smart_feedback_db"
)

# ── Helper ───────────────────────────────────────────────────────
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")

def random_past_date(days_ago_max=90) -> str:
    delta = timedelta(days=random.randint(1, days_ago_max))
    dt = datetime.now(timezone.utc) - delta
    return dt.isoformat()

# ── Seed Data ────────────────────────────────────────────────────
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
if not ADMIN_EMAIL or not ADMIN_PASSWORD:
    raise RuntimeError("Set ADMIN_EMAIL and ADMIN_PASSWORD before running this seeder.")

USERS = [
    # (name, email, student_id, password, department, semester, role)
    ("Admin User",     ADMIN_EMAIL,   None,      ADMIN_PASSWORD,          None,                     None, "admin"),
    ("Arjun Mehta",    "arjun.mehta@college.edu",    "CS2021001","Student@123","Computer Science",         6,    "student"),
    ("Priya Patel",    "priya.patel@college.edu",    "CS2021002","Student@123","Computer Science",         6,    "student"),
    ("Rohan Gupta",    "rohan.gupta@college.edu",    "EC2023001","Student@123","Electronics & Communication",4, "student"),
    ("Sneha Joshi",    "sneha.joshi@college.edu",    "ME2023001","Student@123","Mechanical Engineering",   4,    "student"),
    ("Karan Shah",     "karan.shah@college.edu",     "CS2021003","Student@123","Computer Science",         6,    "student"),
]

COURSES = [
    # (name, department)
    ("Database Management System",    "Computer Science"),
    ("Operating Systems",             "Computer Science"),
    ("Data Structures & Algorithms",  "Computer Science"),
    ("Computer Networks",             "Computer Science"),
    ("Digital Electronics",           "Electronics & Communication"),
    ("Signals and Systems",           "Electronics & Communication"),
    ("Thermodynamics",                "Mechanical Engineering"),
    ("Structural Analysis",           "Civil Engineering"),
]

FACULTY = [
    # (name, department)
    ("Dr. Rajesh Kumar",   "Computer Science"),
    ("Prof. Meena Sharma", "Computer Science"),
    ("Dr. Ankit Verma",    "Electronics & Communication"),
    ("Prof. Sunita Patel", "Mechanical Engineering"),
    ("Dr. Vikram Singh",   "Civil Engineering"),
    ("Prof. Priya Nair",   "Computer Science"),
]

# Feedback samples with pre-known NLP results
# (user_idx, course_idx, faculty_idx, text, anonymous,
#  sentiment_score, sentiment_label, category, urgent)
FEEDBACK_SAMPLES = [
    (1, 0, 0, "The DBMS lectures are well-structured and Dr. Kumar explains every concept with real-world examples. Really enjoying the course.", False,  0.82, "Positive", "Teaching Pace", False),
    (1, 0, 0, "Lab computers in the DBMS lab keep crashing. Many systems have been non-functional for over two weeks. This is seriously affecting our practicals.", False, -0.88, "Negative", "Lab Facilities", True),
    (1, 1, 1, "Operating Systems class moves a little fast. Some students find it hard to keep up with the pace of lectures.", False, -0.42, "Negative", "Teaching Pace", False),
    (1, 2, 5, "DSA lectures are excellent. Prof. Nair uses very clear diagrams and step-by-step walkthroughs. One of the best courses this semester.", False, 0.91, "Positive", "Teaching Pace", False),
    (2, 0, 0, "The DBMS course has not yet covered normalization and transactions which are important exam topics. We are worried about completing the syllabus.", False, -0.63, "Negative", "Syllabus Coverage", False),
    (2, 1, 1, "Operating Systems class is very informative. Prof. Sharma explains process scheduling algorithms clearly.", False, 0.74, "Positive", "Teaching Pace", False),
    (2, 3, 5, "The computer networks lab is okay. Some machines are slow but functional. Could be better.", False, -0.15, "Neutral", "Lab Facilities", False),
    (2, 3, 5, "Computer Networks theory is well paced. Notes provided by the faculty are very helpful for self-study.", True,  0.68, "Positive", "Teaching Pace", False),
    (3, 4, 2, "Digital Electronics lab equipment is outdated. Oscilloscopes are broken in half the lab. Please replace them urgently.", False, -0.90, "Negative", "Lab Facilities", True),
    (3, 4, 2, "Dr. Verma explains digital circuits very well. The examples used in class are practical and relevant.", False, 0.78, "Positive", "Teaching Pace", False),
    (3, 5, 2, "Signals and Systems is a tough subject but the lectures are decent. Would appreciate more practice problems.", False, 0.12, "Neutral", "Syllabus Coverage", False),
    (4, 6, 3, "The classroom used for Thermodynamics has broken ceiling fans. It gets extremely hot during afternoon sessions. This is very uncomfortable.", False, -0.76, "Negative", "Infrastructure", True),
    (4, 6, 3, "Prof. Patel covers the Thermodynamics syllabus thoroughly. All chapters have been completed on time.", True,  0.55, "Positive", "Syllabus Coverage", False),
    (5, 0, 0, "DBMS theory is good but the lab sessions are unproductive because most computers do not have the required software installed.", False, -0.70, "Negative", "Lab Facilities", True),
    (5, 2, 5, "DSA is a well-organized course. The assignments are challenging and helpful for interviews.", False, 0.80, "Positive", "Teaching Pace", False),
    (5, 1, 1, "Some chapters in Operating Systems like memory management have been rushed. We would appreciate spending more time on them.", True, -0.38, "Negative", "Syllabus Coverage", False),
    (1, 3, 5, "The projector in Room 204 has not been working for the past month. Lectures are hard to follow without the slides being visible.", False, -0.65, "Negative", "Infrastructure", False),
    (3, 5, 2, "Overall the Signals and Systems course is satisfactory. Could use more real-world applications in examples.", True,  0.22, "Neutral", "Syllabus Coverage", False),
    (2, 2, 5, "DSA practicals are well-planned. The lab machines are fast and all required IDEs are pre-installed.", False, 0.75, "Positive", "Lab Facilities", False),
    (4, 7, 4, "Structural Analysis lectures by Dr. Singh are very engaging. The hand-drawn diagrams are extremely helpful for understanding concepts.", False, 0.85, "Positive", "Teaching Pace", False),
]


def seed():
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    try:
        # ── Clear existing data ─────────────────────────────────
        print("Clearing existing seed data...")
        cur.execute("DELETE FROM feedback;")
        cur.execute("DELETE FROM faculty;")
        cur.execute("DELETE FROM courses;")
        cur.execute("DELETE FROM users;")
        cur.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1;")
        cur.execute("ALTER SEQUENCE courses_id_seq RESTART WITH 1;")
        cur.execute("ALTER SEQUENCE faculty_id_seq RESTART WITH 1;")
        cur.execute("ALTER SEQUENCE feedback_id_seq RESTART WITH 1;")

        # ── Insert users ────────────────────────────────────────
        print("Inserting users...")
        user_ids = []
        for name, email, student_id, password, dept, sem, role in USERS:
            pw_hash = hash_password(password)
            cur.execute(
                """
                INSERT INTO users (name, email, student_id, password_hash, department, semester, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (name, email, student_id, pw_hash, dept, sem, role)
            )
            user_ids.append(cur.fetchone()[0])
        print(f"  ✓ Inserted {len(user_ids)} users")

        # ── Insert courses ──────────────────────────────────────
        print("Inserting courses...")
        course_ids = []
        for name, dept in COURSES:
            cur.execute(
                "INSERT INTO courses (name, department) VALUES (%s, %s) RETURNING id;",
                (name, dept)
            )
            course_ids.append(cur.fetchone()[0])
        print(f"  ✓ Inserted {len(course_ids)} courses")

        # ── Insert faculty ──────────────────────────────────────
        print("Inserting faculty...")
        faculty_ids = []
        for name, dept in FACULTY:
            cur.execute(
                "INSERT INTO faculty (name, department) VALUES (%s, %s) RETURNING id;",
                (name, dept)
            )
            faculty_ids.append(cur.fetchone()[0])
        print(f"  ✓ Inserted {len(faculty_ids)} faculty")

        # ── Insert feedback ─────────────────────────────────────
        print("Inserting feedback...")
        for (user_idx, course_idx, faculty_idx, text, anon,
             score, label, cat, urgent) in FEEDBACK_SAMPLES:
            created = random_past_date(90)
            cur.execute(
                """
                INSERT INTO feedback
                  (user_id, course_id, faculty_id, feedback_text, anonymous,
                   sentiment_score, sentiment_label, category, urgent, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    user_ids[user_idx],
                    course_ids[course_idx],
                    faculty_ids[faculty_idx],
                    text, anon, score, label, cat, urgent, created
                )
            )
        print(f"  ✓ Inserted {len(FEEDBACK_SAMPLES)} feedback entries")

        conn.commit()
        print("\n✅ Seed data inserted successfully!")
        print("\nDemo login credentials:")
        print("  Student: arjun.mehta@college.edu   / Student@123")
        print("  Student: priya.patel@college.edu   / Student@123")
        print("  Student: rohan.gupta@college.edu   / Student@123")
        print("  Student: sneha.joshi@college.edu   / Student@123")
        print("  Student: karan.shah@college.edu    / Student@123")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    seed()
