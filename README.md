# Finance Discipline

Telegram Mini App для управления личным бюджетом и финансовой дисциплиной.

## Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript, TailwindCSS, Shadcn UI, Recharts
- **Backend**: FastAPI, Python 3.12, SQLAlchemy, Alembic
- **Database**: PostgreSQL 16
- **Auth**: Telegram Login
- **AI**: OpenAI API (optional)
- **Deploy**: Docker, Docker Compose

## Quick Start

```bash
# Clone and start
docker compose up --build
```

Then open http://localhost:3000.

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/v1/        # API endpoints
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── repositories/  # Data access layer
│   ├── alembic/           # DB migrations
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js pages
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom hooks
│   │   ├── lib/           # Utils & API client
│   │   └── types/         # TypeScript types
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Environment Variables

Create `backend/.env`:

```
DATABASE_URL=postgresql+asyncpg://finance:finance@db:5432/finance
SECRET_KEY=your-secret-key
OPENAI_API_KEY=sk-...       # Optional
TELEGRAM_BOT_TOKEN=         # Optional
```

Create `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Features

- Dashboard with balance, monthly stats, financial rating
- Income and expense tracking with categories
- Saving goals with progress tracking
- Budget limits with alerts at 80% and 100%
- Analytics with charts (Pie, Line, Bar)
- AI Advisor with personalized recommendations
- Daily/weekly/monthly notifications
- Gamification with levels and achievements

## API Documentation

With the backend running, visit http://localhost:8000/docs for Swagger UI.
