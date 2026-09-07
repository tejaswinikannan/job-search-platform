# React Jobs

A job board application built with React, React Router, and Tailwind CSS on the frontend, backed by a FastAPI + Pydantic REST API. Users can browse job listings, view details, post new jobs, edit, and delete them.

## Features

- **Home page** — hero section plus quick-action cards linking developers to job listings and employers to the job posting form.
- **Browse jobs** (`/jobs`) — grid of all job listings fetched from the API, with a loading spinner while data is in flight.
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
- [Uvicorn](https://www.uvicorn.org/) as the ASGI server
- Job listings persisted to a local JSON file (`api/data/jobs.json`) — no database required

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
│   ├── routes/jobs.py   # job CRUD endpoints (router mounted at /app/jobs)
│   ├── schemas.py         # Pydantic request/response models (JobCreate, JobUpdate, JobOut, Company)
│   └── storage.py          # reads/writes api/data/jobs.json
├── data/jobs.json    # job listings data store
├── main.py                # FastAPI app entry point
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
| POST   | `/app/jobs/`          | Create a job           |
| GET    | `/app/jobs/{id}`     | Get a single job        |
| PUT    | `/app/jobs/{id}`     | Update a job              |
| DELETE | `/app/jobs/{id}`     | Delete a job                |

FastAPI auto-generates interactive API docs at `http://localhost:8000/docs`.
