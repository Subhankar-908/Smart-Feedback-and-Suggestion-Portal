# Frontend

This folder contains the complete React.js web application.

## Responsibility

- Provides the user interface for both students and administrators.
- Communicates with the backend through REST API calls using Axios.
- Handles routing, authentication state, and role-based page access.

## Technology

| Tool          | Purpose                                    |
|---------------|--------------------------------------------|
| React.js      | UI component framework                     |
| Vite          | Development server and build tool          |
| Tailwind CSS  | Utility-first CSS styling                  |
| React Router  | Client-side routing                        |
| Axios         | HTTP client for API calls                  |
| Recharts      | Chart library for analytics dashboard      |

## Folder Structure (to be created in Phase 10)

```
frontend/
├── src/
│   ├── components/   → Reusable UI components (Navbar, Sidebar, etc.)
│   ├── pages/        → Full page views (Login, Dashboard, AdminDashboard, etc.)
│   ├── services/     → API call functions (api.js)
│   ├── context/      → React Context for global auth state (AuthContext.jsx)
│   ├── App.jsx       → Root component with routing
│   ├── main.jsx      → Entry point
│   └── index.css     → Global styles and Tailwind imports
├── public/           → Static assets
├── package.json      → Project dependencies
└── .env.example      → Sample environment variables
```

## Environment Variables

```
VITE_API_URL=http://localhost:8000
```

## Development

```bash
cd frontend
npm install
npm run dev
```
