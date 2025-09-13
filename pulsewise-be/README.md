## PulseWise Backend (FastAPI)

### Run (Docker)
Service is started by root `docker-compose.yml` and reads env from `.env`.

### Run (Local)
```powershell
cd .\pulsewise-be
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Env (.env)
- `DATABASE_URL`: e.g. `postgresql+psycopg://pulsewise:pulsewise@db:5432/pulsewise`
- `JWT_SECRET`: secret for JWT signing
- `FRONTEND_ORIGIN`: e.g. `http://localhost:8080` (used for CORS)
- `SECRET_KEY`: optional additional secret

### API
- Health: `GET /health`
- Auth:
  - `POST /auth/register` { username/email/password }
  - `POST /auth/login` → returns `{ access_token, user }`
- Diaries & Vitals: `...` (existing)
- Medications: list/create meds, schedules, logs
- Lifestyle: activities, consumptions, symptoms (by diary)
- Education: modules, sections, progress

### Notes
- SQLAlchemy 2.0 + Pydantic v2.
- Consider adding JWT dependency to protect routes next.
