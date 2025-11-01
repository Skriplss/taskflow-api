# TaskFlow API

Production-ready task management REST API built with FastAPI, PostgreSQL, and Docker. Modern backend architecture with JWT authentication, database migrations, comprehensive testing, and CI/CD pipeline.

## Documentation

- [Quick Start Guide](docs/QUICKSTART.md) - Get started in 5 minutes
- [API Examples](docs/API_EXAMPLES.md) - Usage examples with curl, Python, JavaScript
- [Deployment Guide](docs/DEPLOYMENT.md) - Deploy to production
- [Contributing](docs/CONTRIBUTING.md) - Development workflow and guidelines
- [Project Summary](docs/PROJECT_SUMMARY.md) - Architecture overview
- [Changelog](docs/CHANGELOG.md) - Version history

## Features

- **FastAPI** - Modern, fast web framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy 2.0** - Async ORM
- **Alembic** - Database migrations
- **JWT Authentication** - Secure user authentication
- **Docker & Docker Compose** - Containerization
- **Pytest** - Comprehensive testing
- **GitHub Actions** - CI/CD pipeline
- **Pydantic V2** - Data validation
- **Pre-commit hooks** - Code quality

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Tasks
- `GET /api/v1/tasks` - List all tasks (with pagination & filters)
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{id}` - Get task by ID
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `PATCH /api/v1/tasks/{id}/complete` - Mark task as completed

### Health Check
- `GET /health` - Service health status

## Tech Stack

- **Backend**: Python 3.11+, FastAPI 0.104+
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Testing**: Pytest, Pytest-asyncio
- **Containerization**: Docker, Docker Compose
- **Code Quality**: Black, Flake8, isort, mypy, pre-commit

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection and session
│   ├── dependencies.py         # FastAPI dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # API router aggregation
│   │       ├── auth.py         # Authentication endpoints
│   │       └── tasks.py        # Task endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # User SQLAlchemy model
│   │   └── task.py            # Task SQLAlchemy model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py            # User Pydantic schemas
│   │   ├── task.py            # Task Pydantic schemas
│   │   └── token.py           # JWT token schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication business logic
│   │   └── task.py            # Task business logic
│   └── utils/
│       ├── __init__.py
│       ├── security.py        # Password hashing, JWT
│       └── exceptions.py      # Custom exceptions
├── alembic/
│   ├── versions/              # Migration files
│   ├── env.py
│   └── script.py.mako
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures
│   ├── test_auth.py          # Auth endpoint tests
│   └── test_tasks.py         # Task endpoint tests
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI/CD
├── docker-compose.yml
├── docker-compose.dev.yml
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .pre-commit-config.yaml
├── alembic.ini
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd portfolio
```

2. **Create environment file**
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Run with Docker Compose (Recommended)**
```bash
# Development environment
docker-compose -f docker-compose.dev.yml up --build

# Production environment
docker-compose up --build
```

The API will be available at `http://localhost:8000`

4. **Or run locally (without Docker)**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run PostgreSQL (you need it running separately)
# Update .env with your PostgreSQL credentials

# Run migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run tests in Docker
docker-compose exec api pytest
```

## Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - New features (e.g., `feature/add-user-roles`)
- `bugfix/*` - Bug fixes (e.g., `bugfix/fix-auth-token`)
- `hotfix/*` - Production hotfixes

### Workflow Example

```bash
# Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/add-task-priority

# Make changes, commit
git add .
git commit -m "feat: add priority field to tasks"

# Push and create Pull Request
git push origin feature/add-task-priority
```

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "add user table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

## Environment Variables

See `.env.example` for all available configuration options:

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment (development/production) | development |
| `DATABASE_URL` | PostgreSQL connection string | - |
| `SECRET_KEY` | JWT secret key | - |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | 30 |
| `API_V1_PREFIX` | API version prefix | /api/v1 |

## Performance

- Async database operations with SQLAlchemy 2.0
- Connection pooling
- Efficient query pagination
- Response caching (optional)

## Security

- Password hashing with bcrypt
- JWT token-based authentication
- SQL injection prevention (ORM)
- CORS configuration
- Environment-based secrets

## Deployment

### Docker Production Deployment

```bash
# Build production image
docker build -t task-api:latest .

# Run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f api
```

### Manual Deployment

1. Set environment variables for production
2. Run migrations: `alembic upgrade head`
3. Start with production server: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4`

### Recommended Hosting

- **Railway** - Easy deployment with PostgreSQL
- **Render** - Free tier available
- **Heroku** - Classic PaaS
- **DigitalOcean App Platform** - Simple container deployment
- **AWS ECS** - Enterprise-grade

## Future Enhancements

- [ ] Add Redis for caching
- [ ] Implement rate limiting
- [ ] Add WebSocket support for real-time updates
- [ ] Email notifications
- [ ] Task attachments
- [ ] User roles and permissions
- [ ] Task categories and tags
- [ ] GraphQL API
- [ ] Monitoring with Prometheus/Grafana

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.


