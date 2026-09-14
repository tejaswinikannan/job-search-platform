#  Job Board

A job board application built with React, React Router, and Tailwind CSS on the frontend, backed by a FastAPI + Pydantic REST API. Users can browse job listings, view details, post new jobs, edit, and delete them.

## Features

- **Home page** — hero section plus quick-action cards linking developers to job listings and employers to the job posting form.
- **Browse jobs** (`/jobs`) — grid of all job listings fetched from the API, with a loading spinner while data is in flight.
- **Natural-language job search** — a search box on the Browse jobs page lets users type a query like *"remote SQL jobs for a junior dev"* instead of picking dropdown filters. An LLM extracts structured filters (location, job type) and reranks semantically-matched candidates for relevance; see [API](#api) below.
- **Job details** (`/jobs/:id`) — full listing view with job description, salary, location, and company contact info, loaded via a React Router data loader.
- **Add job** (`/add-job`) — form to create a new listing (title, type, description, salary, location, company info) with toast confirmation on submit.
- **Edit job** (`/edit-job/:id`) — form pre-populated with the existing listing's data for updates.
- **Delete job** — remove a listing from its detail page, with a confirmation prompt and toast notification.
- **404 page** for unmatched routes.
- Responsive layout and styling with Tailwind CSS v4, icons via `react-icons`, and toast notifications via `react-toastify`.

## Tech Stack

**Frontend**
- [React 19](https://react.dev/) + [Vite](https://vitejs.dev/)
- [React Router v7](https://reactrouter.com/) (data routers, loaders)
- [Tailwind CSS v4](https://tailwindcss.com/)
- `react-toastify` for notifications, `react-icons` for icons, `react-spinners` for loading states

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) + [Pydantic](https://docs.pydantic.dev/) (Python 3.10+)
- [SQLAlchemy](https://www.sqlalchemy.org/) ORM backed by [SQLite](https://www.sqlite.org/) (`api/data/jobs.db`) — `jobs` and `companies` tables, linked by a foreign key
- [Uvicorn](https://www.uvicorn.org/) as the ASGI server
- [LangChain](https://www.langchain.com/) + OpenAI (`gpt-4o-mini`) for natural-language query parsing and search-result reranking
- [sentence-transformers](https://www.sbert.net/) + [Chroma](https://www.trychroma.com/) for local embedding generation and vector similarity search

## Project Structure

```
frontend/
├── src/
│   ├── components/   # Navbar, Hero, HomeCards, Card, JobListings, JobListing, Spinner, ViewAllJobs
│   ├── layouts/       # MainLayout (Navbar + <Outlet /> + ToastContainer)
│   ├── pages/          # HomePage, JobsPage, JobPage, AddJobPage, EditJobPage, NotFound
│   ├── App.jsx          # Route definitions and API calls (add/update/delete job)
│   └── main.tsx          # App entry point
├── vite.config.ts   # dev server proxy: /api/* -> http://localhost:8000/app/*
└── package.json

api/
├── app/
│   ├── routes/jobs.py   # job CRUD + search endpoints (router mounted at /app/jobs)
│   ├── schemas.py         # Pydantic request/response models (JobCreate, JobUpdate, JobOut, Company)
│   ├── models.py           # SQLAlchemy ORM models (Company, Job) mapped to SQL tables
│   ├── database.py          # engine/session setup + get_db() dependency
│   ├── nlp_search.py         # parse_query() — LLM extracts structured filters from free text
│   ├── vector_search.py       # index_jobs() / semantic_search() — embeddings + Chroma similarity search
│   └── rerank.py                # rerank_jobs() — LLM judges relevance among semantic-search candidates
├── data/
│   ├── jobs.json     # seed data — original listings, read by migrate_data.py
│   └── jobs.db         # SQLite database file (generated, gitignored — not committed)
├── chroma_db/            # persisted vector index (generated, gitignored — rebuild with index_jobs())
├── create_tables.py    # one-off script: builds jobs.db's schema from models.py
├── migrate_data.py       # one-off script: loads jobs.json into jobs.db
├── main.py                 # FastAPI app entry point
├── .env                     # OPENAI_API_KEY (gitignored, not committed)
└── requirements.txt
```

## Getting Started

### 1. Frontend setup

```bash
cd frontend
npm install
```

### 2. Backend setup

```bash
cd api
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```

Then create the database and load the seed data (one-time setup — re-run only if you delete `jobs.db`):

```bash
python create_tables.py
python migrate_data.py
```

Natural-language search needs an OpenAI API key in `api/.env`:

```
OPENAI_API_KEY=sk-...
```

It also needs the job data embedded into the local vector store before it can return results (re-run after adding/editing jobs):

```bash
python -c "from app.database import SessionLocal; from app import models; from app.vector_search import index_jobs; db = SessionLocal(); index_jobs(db.query(models.Job).all())"
```

### Running the app

Two servers, run in separate terminals — both must be running for the app to load job data.

**Terminal 1 — backend:**

```bash
cd frontend
npm run api
```

This starts FastAPI/Uvicorn on `http://localhost:8000` (with `--reload`), using the virtual environment in `api/.venv`.

**Terminal 2 — frontend:**

```bash
cd frontend
npm run dev
```

The Vite dev server proxies requests from `/api/*` to `http://localhost:8000/app/*`, so the browser only ever talks to one origin in development.

## Available Scripts

Run from `frontend/`:

- `npm run dev` — start the Vite development server
- `npm run api` — start the FastAPI backend (`uvicorn main:app --reload`) from `../api`
- `npm run build` — type-check and build for production
- `npm run preview` — preview the production build locally
- `npm run lint` — run ESLint

## API

Base path: `/app/jobs` (proxied through the frontend as `/api/jobs`)

| Method | Path                 | Description         |
|--------|----------------------|----------------------|
| GET    | `/app/jobs/`          | List all jobs         |
| GET    | `/app/jobs/search?query=` | Natural-language search — parses filters, ranks by semantic similarity, reranks by relevance |
| POST   | `/app/jobs/`          | Create a job           |
| GET    | `/app/jobs/{id}`     | Get a single job        |
| PUT    | `/app/jobs/{id}`     | Update a job              |
| DELETE | `/app/jobs/{id}`     | Delete a job                |

`{id}` is an auto-incrementing integer assigned by the database (not a UUID or string).

FastAPI auto-generates interactive API docs at `http://localhost:8000/docs`.
