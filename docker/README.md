# FriedSausages Docker Setup

Docker Compose configuration for running FriedSausages with frontend and backend services.

## Services

- **frontend**: React + Vite dev server on port 5173
- **backend**: FastAPI uvicorn server on port 8000

## Setup

1. Install dependencies:
```bash
npm install
cd backend && pip install -r requirements.txt && cd ..
```

2. Start services:
```bash
docker compose up -d --build
```

3. Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs

## Environment

Frontend connects to backend via `VITE_API_BASE_URL=http://localhost:8000`.

## Development

Hot reload enabled for both frontend and backend. Edit files and changes reflect immediately.

## Stop

```bash
docker compose down
```
