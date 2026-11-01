"""
routes/admin.py
===============
Admin-only analytics and management endpoints:

  GET /api/admin/dashboard  — Summary cards (totals, urgent count)
  GET /api/admin/feedback   — Paginated, filterable feedback table
  GET /api/admin/analytics  — Charts data (sentiment, category, department)
  GET /api/admin/alerts     — Recent urgent feedback items
  GET /api/admin/categories — Category distribution
  GET /api/admin/trends     — Feedback volume over time
  GET /api/admin/insights   — Rule-based actionable insights

All endpoints require admin role (enforced by get_current_admin dependency).
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from app.models.user import User
from app.services.auth_service import get_current_admin
from app.services.analytics_service import (
    get_actionable_insights,
    get_admin_feedback_list,
    get_category_distribution,
    get_dashboard_stats,
    get_department_analysis,
    get_keyword_analysis,
    get_sentiment_distribution,
    get_trends,
    get_urgent_alerts,
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# ─────────────────────────────────────────────────────────────────
# GET /api/admin/dashboard
# ─────────────────────────────────────────────────────────────────
@router.get("/dashboard", summary="Admin dashboard summary statistics")
def admin_dashboard(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Returns summary counts for the top stat cards on the admin dashboard:
    total feedback, positive, neutral, negative, and urgent issues.
    """
    return get_dashboard_stats(db)


# ─────────────────────────────────────────────────────────────────
# GET /api/admin/feedback
# ─────────────────────────────────────────────────────────────────
@router.get("/feedback", summary="Admin feedback management table")
def admin_feedback(
    department: Optional[str]  = Query(None, description="Filter by department"),
    category:   Optional[str]  = Query(None, description="Filter by category"),
    sentiment:  Optional[str]  = Query(None, description="Filter by sentiment label"),
    urgent:     Optional[bool] = Query(None, description="Filter by urgency (true/false)"),
    search:     Optional[str]  = Query(None, description="Search in feedback text"),
    skip:       int            = Query(0,  ge=0),
    limit:      int            = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User     = Depends(get_current_admin),
):
    """
    Returns a paginated, filterable list of all feedback for the admin table.
    Anonymous feedback will show student_name as null.
    """
    return get_admin_feedback_list(
        db, department, category, sentiment, urgent, search, skip, limit
    )


# ─────────────────────────────────────────────────────────────────
# GET /api/admin/analytics
# ─────────────────────────────────────────────────────────────────
@router.get("/analytics", summary="Analytics chart data")
def admin_analytics(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Returns all chart data in one call:
    - sentiment_distribution : for pie/bar chart
    - category_distribution  : for horizontal bar chart
    - department_analysis    : for stacked bar chart
    - keywords               : for keyword cloud/list
    """
    return {
        "sentiment_distribution": get_sentiment_distribution(db),
        "category_distribution":  get_category_distribution(db),
        "department_analysis":    get_department_analysis(db),
        "keywords":               get_keyword_analysis(db),
    }


# ─────────────────────────────────────────────────────────────────
# GET /api/admin/alerts
# ─────────────────────────────────────────────────────────────────
@router.get("/alerts", summary="Urgent feedback alerts")
def admin_alerts(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """Returns the 20 most recent feedback entries flagged as urgent."""
    return get_urgent_alerts(db)


# ─────────────────────────────────────────────────────────────────
# GET /api/admin/categories
# ─────────────────────────────────────────────────────────────────
@router.get("/categories", summary="Category distribution")
def admin_categories(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """Returns feedback count per category, ordered by most frequent."""
    return get_category_distribution(db)


# ─────────────────────────────────────────────────────────────────
# GET /api/admin/trends
# ─────────────────────────────────────────────────────────────────
@router.get("/trends", summary="Feedback volume over time")
def admin_trends(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Returns daily feedback counts for the trend line chart.
    Only includes dates with at least one submission.
    """
    return get_trends(db)


# ─────────────────────────────────────────────────────────────────
# GET /api/admin/insights
# ─────────────────────────────────────────────────────────────────
@router.get("/insights", summary="Actionable insights")
def admin_insights(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Returns rule-based actionable insights for the top problem categories.
    Each insight includes negative feedback percentage and a suggested action.
    """
    return get_actionable_insights(db)
