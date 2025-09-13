## PulseWise Database (Postgres 16)

### Credentials
- DB: `pulsewise`
- User: `pulsewise`
- Password: `pulsewise`
- Port (host): `5433` (mapped to container 5432)

### Initialization
- SQL init scripts in `init/` are executed on first container startup:
  - `01-extensions.sql`
  - `02-schema.sql`

### Connect (psql)
```powershell
psql -h localhost -p 5433 -U pulsewise -d pulsewise
```

### Notes
- Data persisted in Docker volume `db-data`.
- If schema changes, recreate volume or add migrations (Alembic optional).
