# PulseWise

A demo health tracking app with Next.js frontend, FastAPI backend, and Postgres database, orchestrated via Docker Compose and proxied by Nginx.

## Quick Start (Docker)

```powershell
# from repo root
docker compose up --build
```

- App URL: `http://localhost:8080`
- NextAuth endpoints: `http://localhost:8080/api/auth/*`
- Backend API (proxied): `http://localhost:8080/api/*` → FastAPI
- Postgres: `localhost:5433` (host-only)

Stop services:
```powershell
docker compose down
```

## Services

- `db` (Postgres 16)
  - Port: `127.0.0.1:5433 -> 5432`
  - Credentials: `pulsewise` / `pulsewise`
  - Init scripts: `pulsewise-db/init/*.sql`
- `backend` (FastAPI)
  - Reads env from `pulsewise-be/.env`
  - Exposed internally at `pulsewise_backend:8000`
- `frontend` (Next.js)
  - Env via `docker-compose.yml`
  - Exposed internally at `pulsewise_frontend:3000`
- `nginx` (proxy)
  - Public entry: `http://localhost:8080`
  - Routes `/api/auth/*` to frontend (NextAuth)
  - Routes `/api/*` to backend (rewrites `/api/foo` → `/foo`)
  - All else to frontend

## Environment Variables

Backend (`pulsewise-be/.env`):
- `DATABASE_URL` (required): e.g. `postgresql+psycopg://pulsewise:pulsewise@db:5432/pulsewise`
- `JWT_SECRET` (required): secret for JWT signing
- `FRONTEND_ORIGIN` (required): e.g. `http://localhost:8080` for CORS
- `SECRET_KEY` (optional): legacy/random secret

Frontend (compose `frontend.environment`):
- `NEXTAUTH_URL`: `http://localhost:8080/api/auth`
- `NEXTAUTH_SECRET`: secret used by NextAuth (any strong random for dev)
- `NEXT_PUBLIC_API_BASE`: `/api` (Nginx will proxy to backend)

Nginx:
- Uses `nginx/default.conf` that forwards auth and API correctly.

## Local Development (without Docker)

Frontend:
```powershell
cd .\pulsewise-fe
npm install
npm run dev
```
- App: `http://localhost:3000`
- Set local `.env.local` with `NEXTAUTH_URL=http://localhost:3000/api/auth` and `NEXT_PUBLIC_API_BASE=http://localhost:8000`

Backend:
```powershell
cd .\pulsewise-be
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
- Ensure Postgres running and `pulsewise-be/.env` points to it.

Database (Postgres):
- Run via Docker compose or your local instance.
- Connect: `psql -h localhost -p 5433 -U pulsewise -d pulsewise`

## Notes
- If you encounter CORS or auth issues, confirm `FRONTEND_ORIGIN`, `NEXTAUTH_URL`, `NEXT_PUBLIC_API_BASE`, and `JWT_SECRET` align.
- Next.js may warn about multiple lockfiles; prefer running commands from each package dir or set `outputFileTracingRoot` in `pulsewise-fe/next.config.ts`.
