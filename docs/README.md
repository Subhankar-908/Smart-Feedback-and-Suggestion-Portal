# Docs — Project Documentation

This folder contains all project documentation.

## Responsibility

- Documents the system architecture.
- Documents the database design (ER diagram, table descriptions).
- Documents all API endpoints with request/response examples.

## Structure (to be filled across phases)

```
docs/
├── architecture/    → System architecture diagrams and descriptions
├── database/        → ER diagram and database design notes
├── api/             → API endpoint reference with examples
└── README.md        → This file
```

## Documents to Be Created

### Architecture (`docs/architecture/`)

- `system_overview.md` — High-level system diagram showing Frontend → Backend → NLP → Database flow
- `tech_stack.md` — Justification for each technology choice

### Database (`docs/database/`)

- `er_diagram.md` — Entity-relationship diagram
- `table_descriptions.md` — Description of each table and its columns

### API (`docs/api/`)

- `api_reference.md` — Complete list of all API endpoints with:
  - Method and URL
  - Request body / query parameters
  - Response format
  - Authentication requirements
  - Example request and response

## Usage

These documents are intended for:
- Project viva presentation
- Team members onboarding
- Deployment and maintenance reference
