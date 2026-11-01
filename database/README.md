# Database

This folder contains all PostgreSQL database files.

## Files

| File             | Purpose                                                          |
|------------------|------------------------------------------------------------------|
| `schema.sql`     | CREATE TABLE statements with all constraints and relationships   |
| `seed.sql`       | Reference notes for seed data (read this first)                  |
| `seed_helper.py` | Python script that inserts demo data with properly hashed passwords |

## Entity Overview

```
users
 ├── id, name, email, student_id, password_hash
 ├── department, semester, role (student / admin)
 └── created_at

courses
 ├── id, name, department
 └── ← referenced by feedback.course_id

faculty
 ├── id, name, department
 └── ← referenced by feedback.faculty_id

feedback   (core entity)
 ├── user_id → users.id
 ├── course_id → courses.id
 ├── faculty_id → faculty.id
 ├── feedback_text, anonymous
 ├── sentiment_score, sentiment_label, category, urgent   ← NLP results
 └── created_at
```

## How to Set Up

### Step 1 — Create the PostgreSQL database

```sql
psql -U postgres
CREATE DATABASE smart_feedback_db;
\q
```

### Step 2 — Apply the schema

```bash
psql -U postgres -d smart_feedback_db -f schema.sql
```

### Step 3 — Seed demo data

```bash
cd database
# Set these from your backend/.env first; never commit real credentials.
export DATABASE_URL="postgresql://USER:PASSWORD@localhost:5432/smart_feedback_db"
export ADMIN_EMAIL="admin@example.com"
export ADMIN_PASSWORD="use-a-strong-private-password"
pip install psycopg2-binary bcrypt
python seed_helper.py
```

## Credentials and safety

The API creates its administrator from `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `backend/.env`. Do not store production credentials in SQL files or source control. Optional sample students and feedback are available only when `SEED_DEMO_DATA=true` is set for a local demonstration.
