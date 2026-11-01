"""
Smart Feedback Portal — Application Settings
=============================================
Reads configuration from a .env file using pydantic-settings.

Usage:
    from app.config import settings
    print(settings.DATABASE_URL)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables / .env file.
    All fields are read from the environment; defaults are provided for
    development convenience only — override them in .env for production.
    """

    # ── Database ──────────────────────────────────────────────────
    # SQLite works out of the box; set a PostgreSQL URL for deployment.
    DATABASE_URL: str = "sqlite:///./smart_feedback.db"

    # ── JWT / Auth ────────────────────────────────────────────────
    SECRET_KEY: str = "dev-only-change-me-before-deployment"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "ChangeThisAdminPassword!"
    SEED_DEMO_DATA: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",          # Load from .env file in the working directory
        env_file_encoding="utf-8",
        case_sensitive=True,      # DATABASE_URL ≠ database_url
        extra="ignore",           # Silently ignore unknown env vars
    )


# ── Singleton instance ────────────────────────────────────────────
# Import this throughout the app:  from app.config import settings
settings = Settings()

