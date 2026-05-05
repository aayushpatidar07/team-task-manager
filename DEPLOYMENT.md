# Team Task Manager - Railway Deployment Guide

## Quick Start

### 1. Prerequisites
- Railway account (sign up at https://railway.app)
- GitHub account (fork this repository)

### 2. Deploy to Railway

**Option A: Using Railway Dashboard**

1. Go to https://railway.app/dashboard
2. Click "New Project" → "Deploy from GitHub"
3. Select this repository
4. Railway auto-detects Python and reads `Procfile`
5. Click "Deploy" (first deployment uses default values)

**Option B: Using Railway CLI**

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### 3. Configure Environment Variables

In Railway Dashboard:
1. Go to your project
2. Click the app name
3. Go to "Variables" tab
4. Add the following environment variables:

**Essential Variables:**

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | Generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"` | **REQUIRED** - Never commit actual value |
| `CORS_ORIGINS` | `https://yourdomain.com` | Update to your production domain |
| `CREATE_TABLES_ON_STARTUP` | `true` | Set to `false` after first deploy |

### 4. Add MySQL Database

**Using Railway MySQL Plugin (Recommended):**

1. In your Railway project, click "New"
2. Select "Database" → "MySQL"
3. Railway auto-populates `DATABASE_URL` environment variable
4. No additional configuration needed!

**Or using external MySQL:**

1. Set `DATABASE_URL` to your external MySQL connection string
2. Format: `mysql+pymysql://user:password@host:port/database`
3. Ensure the database exists and is accessible from Railway IPs

### 5. Optional: Create Admin User

On first deployment, set these to create an initial admin account:

```
ADMIN_NAME=Admin User
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=change-me-on-first-login
```

**Important**: Remove these variables after first login to prevent re-initialization.

### 6. Domain Configuration

1. In Railway Dashboard, go to your app
2. Click "Settings" → "Environment"
3. Copy the auto-generated Railway URL
4. Update `CORS_ORIGINS` to include your custom domain
5. If using custom domain:
   - Configure DNS to point to Railway
   - Update `CORS_ORIGINS` with your domain

## Deployment Checklist

- [ ] Repository forked on GitHub
- [ ] Railway project created
- [ ] MySQL database added
- [ ] `SECRET_KEY` set to secure random value
- [ ] `DATABASE_URL` configured (auto or manual)
- [ ] `CORS_ORIGINS` updated to production domain
- [ ] Initial deployment successful (check build logs)
- [ ] Access `/healthz` endpoint returns `{"status": "ok"}`
- [ ] Admin user created (if using bootstrap variables)
- [ ] Admin variables removed from environment

## Troubleshooting

### Build Fails
- Check "Build" tab in Railway Dashboard for error logs
- Ensure `requirements.txt` is in project root
- Ensure `Procfile` specifies correct entry point

### Database Connection Error
- Verify `DATABASE_URL` is set correctly
- If using Railway MySQL, wait 1-2 minutes after plugin creation
- Check database is accessible from Railway IPs

### 502 Bad Gateway
- Check app logs in Railway Dashboard
- Verify app is using correct `PORT` environment variable
- Look for Python import or startup errors

### CORS Errors in Browser
- Update `CORS_ORIGINS` to include your frontend domain
- Must include protocol: `https://` not just domain name
- Use comma-separated list for multiple origins: `https://app.com,https://www.app.com`

### Slow First Request
- Railway may take 30-60 seconds to spin up cold container
- Subsequent requests are instant
- Consider upgrading Railway plan for guaranteed resources

## Production Best Practices

1. **Secret Management**
   - Never commit `.env` files
   - Use Railway's built-in environment variable management
   - Rotate `SECRET_KEY` periodically

2. **Database**
   - Use managed MySQL (Railway plugin) in production
   - Enable automatic backups
   - Monitor connection pool size

3. **CORS**
   - Only add trusted frontend origins
   - Use HTTPS in production URLs
   - Remove localhost URLs from production

4. **Admin Account**
   - Change default password immediately after deployment
   - Remove bootstrap variables from environment
   - Consider deleting bootstrap admin user and creating new one

5. **Monitoring**
   - Check Railway Dashboard logs regularly
   - Monitor CPU and memory usage
   - Set up alerts for deploy failures

6. **Security**
   - Use strong, random `SECRET_KEY`
   - Keep `requirements.txt` updated
   - Monitor for security advisories
   - Use HTTPS only (Railway provides auto HTTPS)

## Environment Variables Reference

```bash
# Core
APP_NAME=Team Task Manager
API_V1_PREFIX=/api/v1

# Security (REQUIRED - change in production)
SECRET_KEY=<generate-random-value>
ALGORITHM=HS256

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
DATABASE_URL=mysql+pymysql://user:pass@host:port/db
# OR use these for Railway MySQL plugin:
# MYSQL_USER=<auto>
# MYSQL_PASSWORD=<auto>
# MYSQL_HOST=<auto>
# MYSQL_PORT=<auto>
# MYSQL_DATABASE=<auto>

# CORS (update for your domain)
CORS_ORIGINS=https://yourdomain.com

# Startup
CREATE_TABLES_ON_STARTUP=true

# Optional: Admin Bootstrap (remove after first login)
ADMIN_NAME=Admin User
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=change-me
```

## Architecture

```
┌─────────────────────────────────┐
│       Railway Container         │
│  ┌──────────────────────────┐   │
│  │  Uvicorn (Port 8000)     │   │
│  │  → FastAPI App           │   │
│  │    ├── Auth Routes       │   │
│  │    ├── Project Routes    │   │
│  │    ├── Task Routes       │   │
│  │    └── Static Files      │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
         │
         ↓ (DATABASE_URL)
┌─────────────────────────────────┐
│   Railway MySQL Plugin          │
│   or External MySQL Database    │
└─────────────────────────────────┘
```

## Support

- Railway Docs: https://docs.railway.app
- FastAPI Docs: https://fastapi.tiangolo.com
- SQLAlchemy Docs: https://docs.sqlalchemy.org
- Railway Discord: https://discord.gg/railway
