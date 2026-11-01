"""
tests/backend/test_api_endpoints.py
===================================
End-to-End API and NLP Integration Tests using FastAPI TestClient & SQLite.
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure project root & backend are in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from backend.main import app
from backend.database import Base, get_db
from backend.app.models import User, Course, Faculty, Feedback
from backend.app.services.auth_service import hash_password

# Use an in-memory SQLite database for test isolation
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def init_db():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    # Seed an admin account
    admin_user = User(
        name="Admin User",
        email="admin@test.local",
        password_hash=hash_password("TestAdmin@123"),
        role="admin",
    )
    # Seed course & faculty
    course = Course(name="Database Management System", department="Computer Science")
    faculty = Faculty(name="Dr. Rajesh Kumar", department="Computer Science")

    db.add_all([admin_user, course, faculty])
    db.commit()
    db.close()


@pytest.fixture(autouse=True, scope="module")
def setup_database():
    init_db()
    yield
    Base.metadata.drop_all(bind=test_engine)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_student_registration_and_login():
    # 1. Register student
    reg_payload = {
        "name": "Aarav Sharma",
        "email": "aarav.sharma@college.edu",
        "password": "Password@123",
        "student_id": "CS2022001",
        "department": "Computer Science",
        "semester": 6
    }
    reg_res = client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["role"] == "student"

    # 2. Login with credentials
    login_payload = {
        "email": "aarav.sharma@college.edu",
        "password": "Password@123"
    }
    login_res = client.post("/api/auth/login", json=login_payload)
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

    # 3. Test /me endpoint
    token = login_res.json()["access_token"]
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "aarav.sharma@college.edu"


def test_feedback_submission_and_nlp_pipeline():
    # Login as student
    login_res = client.post("/api/auth/login", json={
        "email": "aarav.sharma@college.edu",
        "password": "Password@123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Submit severe negative lab feedback
    fb_payload = {
        "course_id": 1,
        "faculty_id": 1,
        "feedback_text": "The lab computers are very slow and many systems have stopped working for the last two weeks.",
        "anonymous": True
    }
    fb_res = client.post("/api/feedback/", json=fb_payload, headers=headers)
    assert fb_res.status_code == 201
    fb_data = fb_res.json()

    # Verify NLP results populated automatically
    assert fb_data["sentiment_label"] == "Negative"
    assert fb_data["sentiment_score"] < 0
    assert fb_data["category"] == "Lab Facilities"
    assert fb_data["urgent"] is True
    assert fb_data["anonymous"] is True
    assert fb_data["student_name"] is None  # Hidden because anonymous = True


def test_admin_dashboard_and_role_access():
    # 1. Verify student cannot access admin endpoints (403 Forbidden)
    student_login = client.post("/api/auth/login", json={
        "email": "aarav.sharma@college.edu",
        "password": "Password@123"
    })
    student_token = student_login.json()["access_token"]
    unauth_res = client.get("/api/admin/dashboard", headers={"Authorization": f"Bearer {student_token}"})
    assert unauth_res.status_code == 403

    # 2. Login as Admin
    admin_login = client.post("/api/auth/login", json={
        "email": "admin@test.local",
        "password": "TestAdmin@123"
    })
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 3. Access admin dashboard stats
    dash_res = client.get("/api/admin/dashboard", headers=admin_headers)
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert dash_data["total_feedback"] >= 1
    assert dash_data["negative"] >= 1
    assert dash_data["urgent_issues"] >= 1

    # 4. Access admin feedback list
    list_res = client.get("/api/admin/feedback", headers=admin_headers)
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total"] >= 1
    # Check that anonymous feedback hides student name for admin as well
    first_item = list_data["items"][0]
    if first_item["anonymous"]:
        assert first_item["student_name"] is None

    # 5. Access actionable insights
    ins_res = client.get("/api/admin/insights", headers=admin_headers)
    assert ins_res.status_code == 200
    assert isinstance(ins_res.json(), list)


if __name__ == "__main__":
    init_db()
    test_health_check()
    test_student_registration_and_login()
    test_feedback_submission_and_nlp_pipeline()
    test_admin_dashboard_and_role_access()
    print("ALL Backend & NLP API Integration Tests Passed Successfully!")
