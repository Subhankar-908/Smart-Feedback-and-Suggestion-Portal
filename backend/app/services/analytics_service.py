"""
services/analytics_service.py
==============================
All database queries for the admin analytics dashboard.

Kept separate from routes so queries stay testable in isolation.

Functions:
  get_dashboard_stats()      - Summary counts for the top cards
  get_admin_feedback_list()  - Paginated, filterable feedback table
  get_sentiment_distribution() - For the sentiment pie/bar chart
  get_category_distribution()  - For the category bar chart
  get_department_analysis()    - Department × sentiment breakdown
  get_trends()                 - Feedback volume over time (line chart)
  get_urgent_alerts()          - Most recent urgent feedback items
  get_keyword_analysis()       - Top 20 most frequent meaningful words
  get_actionable_insights()    - Rule-based suggestions per category
"""

import re
from collections import Counter
from typing import Optional

from sqlalchemy import func, desc, case
from sqlalchemy.orm import Session

from app.models import Course, Faculty, Feedback
from app.models.user import User

# ── English stopwords to exclude from keyword analysis ──────────
_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "can", "i", "me", "my",
    "we", "our", "you", "your", "he", "she", "it", "they", "them",
    "this", "that", "these", "those", "and", "but", "or", "so",
    "for", "in", "on", "at", "to", "of", "by", "with", "from",
    "very", "not", "also", "just", "more", "no", "its", "their",
    "there", "here", "which", "who", "what", "how", "all", "some",
    "been", "being", "get", "got", "than", "then", "when", "where",
}

# ── Rule-based insight templates ─────────────────────────────────
_INSIGHTS = {
    "Teaching Pace": {
        "title": "Teaching Pace",
        "common_complaint": "Lectures move too fast; students cannot keep up with concepts.",
        "suggested_action": (
            "Encourage faculty to conduct brief comprehension checks mid-lecture. "
            "Provide recorded sessions or supplementary notes for complex topics."
        ),
    },
    "Lab Facilities": {
        "title": "Lab Facilities",
        "common_complaint": "Computers are slow; required software or hardware is missing or crashing.",
        "suggested_action": (
            "Schedule maintenance for lab PCs. Update IDEs and toolchains. "
            "Ensure all required software is pre-installed before lab sessions."
        ),
    },
    "Canteen & Food": {
        "title": "Canteen & Food Quality",
        "common_complaint": "Unhygienic dining conditions, oily or stale food, or slow food service.",
        "suggested_action": (
            "Conduct surprise food quality inspections with the canteen committee. "
            "Enforce hygiene standards and install water purification servicing."
        ),
    },
    "Placements & Training": {
        "title": "Placements & Training",
        "common_complaint": "Need more company recruitment drives, mock interviews, and aptitude preparation.",
        "suggested_action": (
            "Engage TPO cell to organize industry workshops and coding bootcamps. "
            "Expand corporate outreach for internship and full-time hiring drives."
        ),
    },
    "College Services & Admin": {
        "title": "College Services & Admin",
        "common_complaint": "Long queues at administrative counters, fee processing delays, or bus transport issues.",
        "suggested_action": (
            "Digitize document request processes and optimize bus route schedules. "
            "Set up a dedicated helpdesk counter during peak semester fees periods."
        ),
    },
    "Infrastructure & Hostel": {
        "title": "Infrastructure & Hostel",
        "common_complaint": "Classroom fans, projectors, or hostel water/washroom facilities need repair.",
        "suggested_action": (
            "File prioritized maintenance tickets with the facilities and hostel warden team. "
            "Conduct weekly infrastructure audits across campus."
        ),
    },
    "Infrastructure": {
        "title": "Infrastructure",
        "common_complaint": "Classroom fans, lights, or projectors are broken.",
        "suggested_action": (
            "File maintenance requests with the facilities team. "
            "Prioritize rooms with the most reported issues."
        ),
    },
    "Library Services": {
        "title": "Library Services",
        "common_complaint": "Outdated editions of reference books or lack of quiet study seating.",
        "suggested_action": (
            "Procure latest syllabus reference editions and expand digital journal subscriptions. "
            "Enforce quiet zones in the reading hall."
        ),
    },
    "Syllabus Coverage": {
        "title": "Syllabus Coverage",
        "common_complaint": "Important chapters have not been covered on time before examinations.",
        "suggested_action": (
            "Review semester schedules with department heads. "
            "Identify topics left incomplete and schedule catch-up sessions."
        ),
    },
    "Other": {
        "title": "Other",
        "common_complaint": "Miscellaneous feedback that does not fit a specific category.",
        "suggested_action": "Review individual feedback items for specific action points.",
    },
}


# ─────────────────────────────────────────────────────────────────
# Dashboard Summary
# ─────────────────────────────────────────────────────────────────
def get_dashboard_stats(db: Session) -> dict:
    """Returns total, positive, neutral, negative, and urgent counts."""
    total    = db.query(func.count(Feedback.id)).scalar() or 0
    positive = db.query(func.count(Feedback.id)).filter(Feedback.sentiment_label == "Positive").scalar() or 0
    neutral  = db.query(func.count(Feedback.id)).filter(Feedback.sentiment_label == "Neutral").scalar() or 0
    negative = db.query(func.count(Feedback.id)).filter(Feedback.sentiment_label == "Negative").scalar() or 0
    urgent   = db.query(func.count(Feedback.id)).filter(Feedback.urgent == True).scalar() or 0

    return {
        "total_feedback": total,
        "positive":       positive,
        "neutral":        neutral,
        "negative":       negative,
        "urgent_issues":  urgent,
    }


# ─────────────────────────────────────────────────────────────────
# Admin Feedback List (with filters + pagination)
# ─────────────────────────────────────────────────────────────────
def get_admin_feedback_list(
    db: Session,
    department: Optional[str],
    category:   Optional[str],
    sentiment:  Optional[str],
    urgent:     Optional[bool],
    search:     Optional[str],
    skip:       int,
    limit:      int,
) -> dict:
    """
    Returns a paginated list of feedback entries for the admin table.
    Applies optional filters: department, category, sentiment, urgent, search.
    Anonymous feedback hides the student's name.
    """
    query = (
        db.query(Feedback)
        .join(Course,   Feedback.course_id  == Course.id,   isouter=True)
        .join(Faculty,  Feedback.faculty_id == Faculty.id,  isouter=True)
        .join(User,     Feedback.user_id    == User.id)
    )

    if department:
        query = query.filter(Course.department == department)
    if category:
        query = query.filter(Feedback.category == category)
    if sentiment:
        query = query.filter(Feedback.sentiment_label == sentiment)
    if urgent is not None:
        query = query.filter(Feedback.urgent == urgent)
    if search:
        query = query.filter(Feedback.feedback_text.ilike(f"%{search}%"))

    total = query.count()
    items = (
        query.order_by(desc(Feedback.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = []
    for f in items:
        result.append({
            "id":              f.id,
            "date":            f.created_at.isoformat(),
            "department":      f.course.department     if f.course          else None,
            "course":          f.course.name           if f.course          else None,
            "faculty":         f.faculty.name          if f.faculty         else None,
            "feedback_text":   f.feedback_text,
            "anonymous":       f.anonymous,
            # Never expose student identity for anonymous submissions
            "student_name":    None if f.anonymous else f.user.name,
            "sentiment_label": f.sentiment_label,
            "sentiment_score": f.sentiment_score,
            "category":        f.category,
            "urgent":          f.urgent,
        })

    return {"total": total, "items": result}


# ─────────────────────────────────────────────────────────────────
# Charts
# ─────────────────────────────────────────────────────────────────
def get_sentiment_distribution(db: Session) -> list:
    """Returns count per sentiment label for the pie/bar chart."""
    rows = (
        db.query(Feedback.sentiment_label, func.count(Feedback.id))
        .filter(Feedback.sentiment_label.isnot(None))
        .group_by(Feedback.sentiment_label)
        .all()
    )
    return [{"label": label, "count": count} for label, count in rows]


def get_category_distribution(db: Session) -> list:
    """Returns count per category, ordered by most frequent first."""
    rows = (
        db.query(Feedback.category, func.count(Feedback.id))
        .filter(Feedback.category.isnot(None))
        .group_by(Feedback.category)
        .order_by(func.count(Feedback.id).desc())
        .all()
    )
    return [{"category": cat, "count": count} for cat, count in rows]


def get_department_analysis(db: Session) -> list:
    """
    Returns per-department breakdown of Positive / Neutral / Negative counts.
    Used for the stacked bar chart in the admin dashboard.
    """
    rows = (
        db.query(
            Course.department,
            Feedback.sentiment_label,
            func.count(Feedback.id),
        )
        .join(Course, Feedback.course_id == Course.id)
        .filter(Feedback.sentiment_label.isnot(None))
        .group_by(Course.department, Feedback.sentiment_label)
        .all()
    )

    dept_map: dict = {}
    for dept, sentiment, count in rows:
        if dept not in dept_map:
            dept_map[dept] = {
                "department": dept,
                "Positive":   0,
                "Neutral":    0,
                "Negative":   0,
                "total":      0,
            }
        dept_map[dept][sentiment] = count
        dept_map[dept]["total"] += count

    return list(dept_map.values())


def get_trends(db: Session) -> list:
    """
    Returns daily feedback counts for the trend line chart.
    Works seamlessly across both PostgreSQL and SQLite.
    """
    bind = db.get_bind()
    is_sqlite = bind.dialect.name == "sqlite"

    if is_sqlite:
        date_expr = func.strftime('%Y-%m-%d', Feedback.created_at).label("day_str")
        rows = (
            db.query(
                date_expr,
                func.count(Feedback.id).label("count"),
            )
            .group_by("day_str")
            .order_by("day_str")
            .all()
        )
        return [{"date": str(row.day_str), "count": row.count} for row in rows]
    else:
        rows = (
            db.query(
                func.date_trunc("day", Feedback.created_at).label("day"),
                func.count(Feedback.id).label("count"),
            )
            .group_by("day")
            .order_by("day")
            .all()
        )
        return [{"date": str(row.day.date()), "count": row.count} for row in rows]


# ─────────────────────────────────────────────────────────────────
# Urgent Alerts
# ─────────────────────────────────────────────────────────────────
def get_urgent_alerts(db: Session) -> list:
    """Returns the 20 most recent urgent feedback items."""
    items = (
        db.query(Feedback)
        .join(Course,  Feedback.course_id  == Course.id,  isouter=True)
        .join(Faculty, Feedback.faculty_id == Faculty.id, isouter=True)
        .filter(Feedback.urgent == True)
        .order_by(desc(Feedback.created_at))
        .limit(20)
        .all()
    )
    return [
        {
            "id":              f.id,
            "date":            f.created_at.isoformat(),
            "department":      f.course.department   if f.course         else None,
            "course":          f.course.name         if f.course         else None,
            "faculty":         f.faculty.name        if f.faculty        else None,
            "feedback_text":   f.feedback_text,
            "category":        f.category,
            "sentiment_score": f.sentiment_score,
        }
        for f in items
    ]


# ─────────────────────────────────────────────────────────────────
# Keyword Analysis
# ─────────────────────────────────────────────────────────────────
def get_keyword_analysis(db: Session) -> list:
    """
    Finds the top 20 most frequent meaningful words across all feedback text.
    Uses simple tokenization + stopword removal — no external NLP library needed.
    """
    texts = db.query(Feedback.feedback_text).all()
    word_counter: Counter = Counter()

    for (text,) in texts:
        # Extract only lowercase alphabetic words of length >= 3
        words = re.findall(r"\b[a-z]{3,}\b", text.lower())
        meaningful = [w for w in words if w not in _STOPWORDS]
        word_counter.update(meaningful)

    return [
        {"word": word, "count": count}
        for word, count in word_counter.most_common(20)
    ]


# ─────────────────────────────────────────────────────────────────
# Actionable Insights
# ─────────────────────────────────────────────────────────────────
def get_actionable_insights(db: Session) -> list:
    """
    Generates rule-based actionable insights for the top problem categories.

    Logic:
    1. Find categories with the most negative feedback.
    2. Compute the negative feedback percentage for each.
    3. Return the top insights with a suggested action.
    """
    rows = (
        db.query(
            Feedback.category,
            func.count(Feedback.id).label("total"),
            func.sum(
                case((Feedback.sentiment_label == "Negative", 1), else_=0)
            ).label("negative_count"),
        )
        .filter(Feedback.category.isnot(None))
        .group_by(Feedback.category)
        .order_by(desc("negative_count"))
        .limit(5)
        .all()
    )

    insights = []
    for category, total, neg_count in rows:
        neg_count = neg_count or 0
        neg_pct   = round((neg_count / total) * 100, 1) if total > 0 else 0
        template  = _INSIGHTS.get(category, _INSIGHTS["Other"])
        insights.append({
            "category":         category,
            "total_feedback":   total,
            "negative_count":   neg_count,
            "negative_percent": neg_pct,
            "common_complaint": template["common_complaint"],
            "suggested_action": template["suggested_action"],
        })

    return insights
