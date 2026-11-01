# REST API Specification

Base URL: `http://localhost:8000/api`  
Interactive Swagger Documentation: `http://localhost:8000/api/docs`

---

## 1. Authentication Endpoints

### `POST /api/auth/register`
Creates a student account and returns an access token immediately.
- **Request Body**:
  ```json
  {
    "name": "Arjun Mehta",
    "email": "arjun@college.edu",
    "password": "Password@123",
    "student_id": "CS2022001",
    "department": "Computer Science",
    "semester": 6
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "name": "Arjun Mehta",
      "email": "arjun@college.edu",
      "student_id": "CS2022001",
      "department": "Computer Science",
      "semester": 6,
      "role": "student",
      "created_at": "2026-09-02T10:00:00Z"
    }
  }
  ```

### `POST /api/auth/login`
Authenticates a user and returns a signed JWT token.
- **Request Body**:
  ```json
  {
    "email": "your-admin-email-from-backend-env",
    "password": "your-admin-password-from-backend-env"
  }
  ```

### `GET /api/auth/me`
Returns current authenticated user profile.
- **Headers**: `Authorization: Bearer <token>`

---

## 2. Student Feedback Endpoints

### `GET /api/feedback/departments`
Returns distinct department names.

### `GET /api/feedback/courses?department=Computer%20Science`
Returns courses filtered by department.

### `GET /api/feedback/faculty?department=Computer%20Science`
Returns faculty members filtered by department.

### `POST /api/feedback`
Submits feedback, runs the NLP pipeline in real-time, and stores results.
- **Headers**: `Authorization: Bearer <token>` (Student Only)
- **Request Body**:
  ```json
  {
    "course_id": 1,
    "faculty_id": 1,
    "feedback_text": "The lab computers are broken and sparking smoke.",
    "anonymous": true
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "id": 42,
    "course_id": 1,
    "faculty_id": 1,
    "feedback_text": "The lab computers are broken and sparking smoke.",
    "anonymous": true,
    "sentiment_score": -0.85,
    "sentiment_label": "Negative",
    "category": "Lab Facilities",
    "urgent": true,
    "created_at": "2026-09-02T10:30:00Z",
    "student_name": null,
    "course_name": "Database Management System",
    "faculty_name": "Dr. Rajesh Kumar",
    "department": "Computer Science"
  }
  ```

### `GET /api/feedback/my`
Returns authenticated student's submission history.

---

## 3. Administrator Endpoints

### `GET /api/admin/dashboard`
Returns high-level summary counters:
```json
{
  "total_feedback": 120,
  "positive": 75,
  "neutral": 25,
  "negative": 20,
  "urgent_issues": 4
}
```

### `GET /api/admin/analytics`
Returns chart data: `sentiment_distribution`, `category_distribution`, `department_analysis`, and `keywords`.

### `GET /api/admin/alerts`
Returns up to 20 most recent feedback entries marked as urgent.

### `GET /api/admin/insights`
Returns actionable insights and administrative recommendations.

### `GET /api/admin/feedback?department=&category=&sentiment=&urgent=&search=&skip=0&limit=15`
Paginated and filterable feedback management table.
