## PulseWise Frontend (Next.js)

### Dev run
```powershell
cd .\pulsewise-fe
npm install
npm run dev
```
App at `http://localhost:3000`.

### Production build
```powershell
npm run build
npm start
```

### Environment
- `NEXTAUTH_URL` (dev): `http://localhost:3000/api/auth` (or via Nginx at `http://localhost:8080/api/auth` when using Docker)
- `NEXTAUTH_SECRET`: any random string for dev
- `NEXT_PUBLIC_API_BASE`: `/api` when proxied by Nginx, or `http://localhost:8000` when running backend directly

### Docker
Env is provided by `docker-compose.yml`:
- `NEXTAUTH_URL=http://localhost:8080/api/auth`
- `NEXTAUTH_SECRET=dev_secret_change_me`
- `NEXT_PUBLIC_API_BASE=/api`

### Notes
- NextAuth Credentials provider is configured in `app/api/auth/[...nextauth]/route.ts`.
- UI components live under `components/ui` and a `NavBar` in `components/NavBar.tsx`.
