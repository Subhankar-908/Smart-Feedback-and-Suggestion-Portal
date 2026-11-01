# System Architecture & Design

## 1. High-Level Architecture Overview

The **Smart Feedback & Suggestion Portal** follows a modern, decoupled client-server architecture with dedicated Natural Language Processing (NLP) intelligence:

```
┌─────────────────────────────────────────────────────────┐
│              Client Layer (React.js + Vite)             │
│   • Student Portal (Form, History, Live NLP feedback)   │
│   • Admin Portal (Analytics, Recharts, Filters, Alerts) │
└────────────────────────────┬────────────────────────────┘
                             │ HTTP / JSON (REST API)
                             │ JWT Authorization Header
┌────────────────────────────▼────────────────────────────┐
│               Backend Layer (Python + FastAPI)          │
│   • Authentication & RBAC (Student vs Admin)            │
│   • Feedback Endpoints & CRUD Operations                │
│   • Analytics Service (Aggregations, Insights, Trends)  │
└──────────────┬───────────────────────────┬──────────────┘
               │                           │
┌──────────────▼──────────────┐ ┌──────────▼──────────────┐
│       Database Layer        │ │       NLP Pipeline      │
│   • PostgreSQL (SQLAlchemy) │ │   • Text Preprocessing  │
│   • Users, Courses,         │ │   • VADER Sentiment     │
│     Faculty, Feedback       │ │   • Category Classifier │
│   • Referential Integrity   │ │   • Urgent Detector     │
└─────────────────────────────┘ └─────────────────────────┘
```

---

## 2. Key Component Responsibilities

### A. Frontend (React 18 + Vite + Tailwind CSS)
- **Role-Based Views**: Student Dashboard vs. Admin Analytics.
- **Visual Analytics**: Interactive Recharts (Pie, Bar, Stacked Bar, Line charts).
- **Security & Session**: JWT stored securely in `localStorage`, attached via Axios request interceptors, with automatic session expiry handling.
- **Privacy Assurance**: Clear visual indicators for Anonymous vs Public submissions.

### B. Backend API (FastAPI + SQLAlchemy)
- **High Performance**: Asynchronous ASGI server (`uvicorn`) for fast request throughput.
- **Data Validation**: Strict Pydantic v2 schemas for all inputs and responses.
- **Authentication**: Direct `bcrypt` password hashing (12 salt rounds) + cryptographically signed HS256 JWT tokens.
- **Anonymity Protection**: Strips student identity on anonymous submissions across all API responses.

### C. NLP Intelligence Engine (`ml/`)
- **Text Cleaning**: Lowercasing, URL/email stripping, regex tokenization, stopword removal with negation preservation, and WordNet lemmatization.
- **Sentiment Analysis**: VADER compound scoring with institutional domain lexicon tuning.
- **Category Classification**: Domain phrase matching and keyword token scoring for 5 operational areas.
- **Urgency Detection**: Detects severe negative issues, prolonged downtime, and hazardous conditions.

---

## 3. Technology Stack Rationale

| Layer | Chosen Technology | Rationale |
|---|---|---|
| **Frontend** | React 18 + Vite | Fast HMR development, component reusability, single-page app responsiveness. |
| **Styling & Icons** | Tailwind CSS + Lucide React | Clean, responsive UI with zero bloated stylesheets. |
| **Visual Charts** | Recharts | Declarative, SVG-based charts with smooth animations and tooltips. |
| **Backend API** | FastAPI | High performance, automatic OpenAPI `/docs` documentation, native Pydantic validation. |
| **Database** | PostgreSQL + SQLAlchemy | ACID compliance, strong relational integrity (Foreign Keys, cascading rules, check constraints). |
| **NLP Engine** | NLTK + VADER | Fast, deterministic, explainable for college viva, requires zero expensive GPU training. |
