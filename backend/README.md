# Backend

FastAPI REST API with SQLAlchemy, JWT auth, role guards, and NLP integration.

Run from this directory:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

API docs: http://localhost:8000/api/docs
Health: http://localhost:8000/api/health

SQLite is the local default. Set `DATABASE_URL` to a PostgreSQL connection string for deployment. Configure `SECRET_KEY`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and `CORS_ORIGINS` in `.env`.
