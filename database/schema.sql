-- ============================================================
-- Smart Feedback & Suggestion Portal
-- PostgreSQL Database Schema
-- ============================================================
-- Run with: psql -d smart_feedback_db -f schema.sql
-- ============================================================

-- Drop tables in reverse dependency order if re-running
DROP TABLE IF EXISTS feedback CASCADE;
DROP TABLE IF EXISTS faculty CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================================
-- TABLE: users
-- Stores both student and admin accounts.
-- Role distinguishes between the two.
-- ============================================================
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    email           VARCHAR(150) UNIQUE NOT NULL,
    student_id      VARCHAR(20)  UNIQUE,                    -- Only for students
    password_hash   VARCHAR(255) NOT NULL,
    department      VARCHAR(100),
    semester        INTEGER CHECK (semester BETWEEN 1 AND 8),
    role            VARCHAR(10)  NOT NULL DEFAULT 'student'
                        CHECK (role IN ('student', 'admin')),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- TABLE: courses
-- Courses offered at the institution.
-- ============================================================
CREATE TABLE courses (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL,
    department  VARCHAR(100) NOT NULL
);

-- ============================================================
-- TABLE: faculty
-- Faculty members across departments.
-- ============================================================
CREATE TABLE faculty (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    department  VARCHAR(100) NOT NULL
);

-- ============================================================
-- TABLE: feedback
-- Core entity. Stores feedback text + NLP analysis results.
-- ============================================================
CREATE TABLE feedback (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL
                        REFERENCES users(id) ON DELETE CASCADE,
    course_id       INTEGER
                        REFERENCES courses(id) ON DELETE SET NULL,
    faculty_id      INTEGER
                        REFERENCES faculty(id) ON DELETE SET NULL,
    feedback_text   TEXT NOT NULL,
    anonymous       BOOLEAN NOT NULL DEFAULT FALSE,

    -- NLP results (populated by the NLP pipeline after submission)
    sentiment_score FLOAT,
    sentiment_label VARCHAR(10)
                        CHECK (sentiment_label IN ('Positive', 'Neutral', 'Negative')),
    category        VARCHAR(30)
                        CHECK (category IN (
                            'Teaching Pace',
                            'Lab Facilities',
                            'Canteen & Food',
                            'Placements & Training',
                            'College Services & Admin',
                            'Infrastructure & Hostel',
                            'Library Services',
                            'Syllabus Coverage',
                            'Infrastructure',
                            'Other'
                        )),
    urgent          BOOLEAN NOT NULL DEFAULT FALSE,

    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- INDEXES
-- For frequently queried columns in dashboard/analytics queries
-- ============================================================
CREATE INDEX idx_feedback_user_id        ON feedback(user_id);
CREATE INDEX idx_feedback_sentiment      ON feedback(sentiment_label);
CREATE INDEX idx_feedback_category       ON feedback(category);
CREATE INDEX idx_feedback_urgent         ON feedback(urgent);
CREATE INDEX idx_feedback_created_at     ON feedback(created_at);
CREATE INDEX idx_feedback_anonymous      ON feedback(anonymous);
CREATE INDEX idx_users_email             ON users(email);
CREATE INDEX idx_users_role              ON users(role);
CREATE INDEX idx_courses_department      ON courses(department);
CREATE INDEX idx_faculty_department      ON faculty(department);
