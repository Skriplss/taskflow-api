# Quick Start Guide

Get TaskFlow API running in 5 minutes.

## Fastest Method (Docker)

### Prerequisites
- Docker and Docker Compose installed
- Git installed

### Steps

1. **Clone and enter directory**
   ```bash
   git clone <your-repo-url>
   cd portfolio
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Start everything with Docker**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

4. **API is ready!**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health

### Test it out

```bash
# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123"}'

# Login and get token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

## Local Development (Without Docker)

### Prerequisites
- Python 3.11+
- PostgreSQL 15 installed and running

### Steps

1. **Clone repository**
   ```bash
   git clone <your-repo-url>
   cd portfolio
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Create PostgreSQL database**
   ```bash
   createdb taskdb
   ```

5. **Create .env file**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and update:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/taskdb
   DATABASE_URL_SYNC=postgresql://postgres:yourpassword@localhost:5432/taskdb
   SECRET_KEY=your-secret-key-run-openssl-rand-hex-32
   ```

6. **Run migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Visit**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## Run Tests

```bash
# With virtual environment activated
pytest

# With coverage
pytest --cov=app --cov-report=html

# With Docker
docker-compose exec api pytest
```

## Using Makefile (Recommended)

If you have `make` installed:

```bash
# Complete setup
make setup

# Run with Docker
make run-dev

# Run tests
make test

# Format code
make format

# View all commands
make help
```

## Create First Migration

After modifying models:

```bash
# Create migration
alembic revision --autogenerate -m "add new field"

# Apply migration
alembic upgrade head
```

## Next Steps

1. Read the full README.md for detailed information
2. Check API_EXAMPLES.md for usage examples
3. Review DEPLOYMENT.md for production deployment
4. Explore the API at http://localhost:8000/docs

## Troubleshooting

### Port 8000 already in use
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --reload --port 8001
```

### Database connection error
```bash
# Check PostgreSQL is running
pg_isready

# Verify database exists
psql -l | grep taskdb
```

### Docker issues
```bash
# Clean up and restart
docker-compose down -v
docker-compose -f docker-compose.dev.yml up --build
```

### Migration errors
```bash
# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d db
docker-compose exec api alembic upgrade head
```

## Tips

- Use Swagger UI at `/docs` for interactive API testing
- Check logs if something doesn't work: `docker-compose logs -f`
- The dev environment has hot reload enabled
- Default credentials in tests: `testuser` / `testpassword123`

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub

