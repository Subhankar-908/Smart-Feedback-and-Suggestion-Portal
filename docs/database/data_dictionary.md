# Database Schema & Data Dictionary

## 1. Entity-Relationship (ER) Overview

```
┌─────────────────────┐             ┌────────────────────────┐
│        users        │             │        courses         │
├─────────────────────┤             ├────────────────────────┤
│ id (PK)             │             │ id (PK)                │
│ name                │             │ name                   │
│ email (UNIQUE)      │             │ department (INDEX)     │
│ student_id (UNIQUE) │             └───────────┬────────────┘
│ password_hash       │                         │
│ department          │                         │ 1:N
│ semester (1-8)      │                         │
│ role (student/admin)│                         │
│ created_at          │                         │
└──────────┬──────────┘                         │
           │                                    │
           │ 1:N (CASCADE)                      │
           │                                    │
           │         ┌──────────────────────────▼┐
           └────────►│         feedback          │◄──────────┐
                     ├───────────────────────────┤           │
                     │ id (PK)                   │           │
                     │ user_id (FK → users)      │           │ 1:N
                     │ course_id (FK → courses)  │           │
                     │ faculty_id (FK → faculty) ├───────────┘
                     │ feedback_text             │ ┌────────────────────┐
                     │ anonymous (BOOLEAN)       │ │      faculty       │
                     │ sentiment_score (FLOAT)   │ ├────────────────────┤
                     │ sentiment_label (VARCHAR) │ │ id (PK)            │
                     │ category (VARCHAR)        │ │ name               │
                     │ urgent (BOOLEAN)          │ │ department (INDEX) │
                     │ created_at (TIMESTAMP)    │ └────────────────────┘
                     └───────────────────────────┘
```

---

## 2. Table Specifications

### 1. `users` Table
Stores user accounts for both students and administrators.
- `id` (SERIAL PRIMARY KEY)
- `name` (VARCHAR(100), NOT NULL)
- `email` (VARCHAR(150), UNIQUE, NOT NULL, INDEXED)
- `student_id` (VARCHAR(20), UNIQUE, NULL for admins)
- `password_hash` (VARCHAR(255), NOT NULL, direct bcrypt hash)
- `department` (VARCHAR(100))
- `semester` (INTEGER, CHECK: `semester BETWEEN 1 AND 8`)
- `role` (VARCHAR(10), NOT NULL, CHECK: `role IN ('student', 'admin')`)
- `created_at` (TIMESTAMP WITH TIME ZONE, DEFAULT NOW())

### 2. `courses` Table
Master table of academic courses.
- `id` (SERIAL PRIMARY KEY)
- `name` (VARCHAR(150), NOT NULL)
- `department` (VARCHAR(100), NOT NULL, INDEXED)

### 3. `faculty` Table
Master table of faculty members and facilities.
- `id` (SERIAL PRIMARY KEY)
- `name` (VARCHAR(150), NOT NULL)
- `department` (VARCHAR(100), NOT NULL, INDEXED)

### 4. `feedback` Table
Core feedback records with embedded NLP analysis.
- `id` (SERIAL PRIMARY KEY)
- `user_id` (INTEGER, FK → `users.id` ON DELETE CASCADE)
- `course_id` (INTEGER, FK → `courses.id` ON DELETE SET NULL)
- `faculty_id` (INTEGER, FK → `faculty.id` ON DELETE SET NULL)
- `feedback_text` (TEXT, NOT NULL)
- `anonymous` (BOOLEAN, DEFAULT FALSE, INDEXED)
- `sentiment_score` (FLOAT, Range -1.0 to +1.0)
- `sentiment_label` (VARCHAR(10), CHECK: `sentiment_label IN ('Positive', 'Neutral', 'Negative')`)
- `category` (VARCHAR(30), CHECK: `category IN ('Teaching Pace', 'Lab Facilities', 'Syllabus Coverage', 'Infrastructure', 'Other')`)
- `urgent` (BOOLEAN, DEFAULT FALSE, INDEXED)
- `created_at` (TIMESTAMP WITH TIME ZONE, DEFAULT NOW(), INDEXED)
