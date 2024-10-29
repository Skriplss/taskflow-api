# Deployment Guide

This guide covers deploying TaskFlow API to various platforms.

## Quick Deploy Options

### Option 1: Railway (Recommended for Beginners)

[Railway](https://railway.app) offers easy deployment with PostgreSQL included.

1. **Create Railway account** at https://railway.app

2. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

3. **Initialize project**
   ```bash
   railway init
   ```

4. **Add PostgreSQL**
   ```bash
   railway add postgresql
   ```

5. **Set environment variables**
   ```bash
   railway variables set SECRET_KEY=$(openssl rand -hex 32)
   railway variables set ENVIRONMENT=production
   ```

6. **Deploy**
   ```bash
   railway up
   ```

Your API will be available at: `https://your-app.railway.app`

### Option 2: Render

[Render](https://render.com) provides free tier with PostgreSQL.

1. **Create account** at https://render.com

2. **Create PostgreSQL database**
   - Go to Dashboard → New → PostgreSQL
   - Copy the Internal Database URL

3. **Create Web Service**
   - Go to Dashboard → New → Web Service
   - Connect your GitHub repository
   - Configure:
     - **Environment**: Docker
     - **Plan**: Free (or paid for production)
     - **Environment Variables**:
       ```
       DATABASE_URL=<internal-database-url>
       DATABASE_URL_SYNC=<internal-database-url-without-async>
       SECRET_KEY=<generate-with-openssl-rand-hex-32>
       ENVIRONMENT=production
       ```

4. **Deploy** - Render will automatically deploy on push to main

### Option 3: Heroku

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   heroku login
   ```

2. **Create app and add PostgreSQL**
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:mini
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=$(openssl rand -hex 32)
   heroku config:set ENVIRONMENT=production
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Run migrations**
   ```bash
   heroku run alembic upgrade head
   ```

### Option 4: DigitalOcean App Platform

1. **Create account** at https://www.digitalocean.com

2. **Create App**
   - Connect GitHub repository
   - Choose Docker as deployment method

3. **Add Database**
   - Add PostgreSQL Dev Database (or Production)

4. **Configure environment variables**

5. **Deploy** - Auto-deploys on git push

### Option 5: AWS (Advanced)

For AWS deployment using ECS:

1. **Create ECR repository**
   ```bash
   aws ecr create-repository --repository-name task-api
   ```

2. **Build and push Docker image**
   ```bash
   docker build -t task-api .
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   docker tag task-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/task-api:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/task-api:latest
   ```

3. **Create RDS PostgreSQL instance**

4. **Create ECS cluster and service**

5. **Configure Load Balancer and Auto Scaling**

## Environment Variables for Production

Required environment variables:

```bash
# Application
ENVIRONMENT=production
DEBUG=False
APP_NAME="Task Management API"

# API
API_V1_PREFIX=/api/v1

# Database (from your hosting provider)
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
DATABASE_URL_SYNC=postgresql://user:password@host:5432/dbname

# Security (generate with: openssl rand -hex 32)
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (add your frontend domain)
BACKEND_CORS_ORIGINS=["https://your-frontend.com"]
```

## Database Migrations

After deployment, run migrations:

```bash
# Railway
railway run alembic upgrade head

# Render (SSH into container)
alembic upgrade head

# Heroku
heroku run alembic upgrade head

# Docker
docker-compose exec api alembic upgrade head
```

## Security Checklist

Before going to production:

- [ ] Set strong `SECRET_KEY` (use `openssl rand -hex 32`)
- [ ] Set `DEBUG=False`
- [ ] Configure proper CORS origins
- [ ] Use HTTPS (most platforms provide this automatically)
- [ ] Set up database backups
- [ ] Configure environment variables (never commit secrets)
- [ ] Review and update `.env` file
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting (if needed)
- [ ] Review security headers
- [ ] Set up SSL/TLS certificates

## Monitoring and Logging

### Add logging to production

Update `app/main.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Recommended monitoring tools:

- **Sentry** - Error tracking
- **New Relic** - Application monitoring
- **Datadog** - Infrastructure monitoring
- **LogRocket** - User session replay

## CI/CD Setup

The project includes GitHub Actions CI/CD. To use it:

1. **Add secrets to GitHub**:
   - Go to repository Settings → Secrets
   - Add: `SECRET_KEY`, database credentials, etc.

2. **Automatic deployment**:
   - Push to `main` branch triggers production deploy
   - Push to `develop` branch triggers staging deploy
   - Pull requests run tests automatically

## Testing Production

After deployment, test your API:

```bash
# Health check
curl https://your-api.com/health

# Register user
curl -X POST https://your-api.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"testpass123"}'

# Login
curl -X POST https://your-api.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

## Docker Production Deployment

For self-hosted production:

```bash
# Build production image
docker build -t task-api:production .

# Run with docker-compose
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f api

# Run migrations
docker-compose exec api alembic upgrade head
```

## Scaling

### Horizontal Scaling

1. Use load balancer (nginx, HAProxy, or cloud provider's LB)
2. Run multiple API instances
3. Use connection pooling for database
4. Add Redis for caching and sessions

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Add database indexes
- Use CDN for static assets

## Troubleshooting

### Common Issues

**Database connection errors:**
- Check `DATABASE_URL` format
- Verify database is running
- Check firewall rules

**Migration errors:**
- Ensure migrations are up to date
- Check database permissions
- Review Alembic logs

**Authentication errors:**
- Verify `SECRET_KEY` is set
- Check JWT token expiration
- Review CORS settings

## Additional Resources

- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [PostgreSQL Backup Guide](https://www.postgresql.org/docs/current/backup.html)
- [Security Best Practices](https://owasp.org/www-project-api-security/)

## Support

If you encounter issues:

1. Check application logs
2. Review this deployment guide
3. Check GitHub Issues
4. Contact the development team

