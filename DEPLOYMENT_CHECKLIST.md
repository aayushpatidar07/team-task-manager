# Team Task Manager - Production Deployment Checklist

## Pre-Deployment

- [ ] Git repository initialized and all files committed
- [ ] `.env` and `.env.*.local` added to `.gitignore`
- [ ] No hardcoded secrets in code or environment files
- [ ] All tests pass locally (`python -m pytest` or similar)
- [ ] `python -m compileall app` shows no errors
- [ ] Database migrations planned (if applicable)

## Railway Configuration

- [ ] Railway account created and project initialized
- [ ] GitHub repository connected to Railway
- [ ] Railway environment variables configured:
  - [ ] `SECRET_KEY` - set to secure random value
  - [ ] `CORS_ORIGINS` - updated to production domain (https://)
  - [ ] `CREATE_TABLES_ON_STARTUP` - set to `true` for initial deploy
  - [ ] `DATABASE_URL` - configured (auto if using Railway MySQL plugin)
- [ ] MySQL database provisioned (Railway plugin or external)
- [ ] Database credentials verified and accessible

## Initial Deployment

- [ ] Procfile present in repository root
- [ ] `Procfile` specifies correct command: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] `requirements.txt` includes all dependencies
- [ ] First deployment completes without errors
- [ ] Check deployment logs for startup messages
- [ ] Verify app is running: curl `https://<railway-url>/healthz`
- [ ] Expected response: `{"status":"ok"}`

## Database Initialization

- [ ] Tables created (auto if `CREATE_TABLES_ON_STARTUP=true`)
- [ ] Admin user created (if bootstrap variables set)
- [ ] Database verified: `curl -X GET https://<railway-url>/api/v1/auth/me -H "Authorization: Bearer <admin-token>"`

## Frontend Integration

- [ ] Frontend app deployed or accessible
- [ ] `CORS_ORIGINS` includes frontend URL(s)
- [ ] Frontend can login and create token
- [ ] Frontend can call protected endpoints
- [ ] Test full user flow: Register → Login → Create Task

## Security Hardening

- [ ] Remove bootstrap admin variables (`ADMIN_NAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`)
- [ ] Verify no debug mode enabled
- [ ] Check security headers present: `X-Content-Type-Options: nosniff`
- [ ] HTTPS enforced (Railway provides auto HTTPS)
- [ ] CORS origins limited to trusted domains only
- [ ] `CREATE_TABLES_ON_STARTUP` set to `false` after initial deploy

## Monitoring & Maintenance

- [ ] Enable Railway logs and review for errors
- [ ] Set up alerts for deploy failures
- [ ] Monitor CPU and memory usage
- [ ] Plan database backup strategy
- [ ] Document rollback procedure
- [ ] Create runbook for common issues

## Post-Deployment Verification

- [ ] Health check endpoint responds (`/healthz`)
- [ ] Authentication endpoints working:
  - [ ] POST `/api/v1/auth/register` - creates account
  - [ ] POST `/api/v1/auth/login` - returns token
  - [ ] GET `/api/v1/auth/me` - requires valid token
- [ ] Admin endpoints restricted:
  - [ ] POST `/api/v1/projects` - requires admin
  - [ ] GET `/api/v1/tasks` - member sees assigned only
- [ ] Static files served: `/` loads index.html
- [ ] Error handling returns proper status codes
- [ ] Database connection stable under load

## Rollback Plan

- [ ] Previous deployment available in Railway history
- [ ] Can rollback to previous version in <5 minutes
- [ ] Database backups available for point-in-time recovery
- [ ] Manual rollback instructions documented

## Known Issues & Workarounds

### Cold Start
- First request may take 30-60 seconds (Railway container spinup)
- Subsequent requests are fast
- Consider upgrading Railway plan for guaranteed resources

### Port Configuration
- Railway sets `$PORT` environment variable dynamically
- Procfile must use `$PORT` variable, not hardcoded port
- Uvicorn must bind to `0.0.0.0` for Railway networking

### Database Connection
- MySQL driver requires `pymysql` (not `mysqldb`)
- Connection pooling configured in SQLAlchemy
- Railway MySQL plugin auto-populates `DATABASE_URL`

## Environment Variables Summary

| Variable | Local Dev | Staging | Production | Notes |
|----------|-----------|---------|------------|-------|
| `SECRET_KEY` | random | random | **SECURE** | Generate new for production |
| `CORS_ORIGINS` | localhost | staging.com | yourdomain.com | Update for your domain |
| `CREATE_TABLES_ON_STARTUP` | true | true | false | Disable after schema set |
| `DATABASE_URL` | local MySQL | managed DB | Railway MySQL | Use Railway plugin if available |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 60 | 60 | 60+ | Adjust as needed |

## Deployment History

| Date | Version | Changes | Status |
|------|---------|---------|--------|
| | | | |

## Support Contacts

- Railway Support: support@railway.app
- Repository Issues: [GitHub Issues]
- Internal Team: [Team Contact Info]
