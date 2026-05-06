# Railway Deployment Guide 🚀

Complete step-by-step guide to deploy Team Task Manager on Railway.

## Prerequisites ✅

- GitHub account with your repository pushed
- Railway account (free tier available at https://railway.app)
- Your repository is public or Railway has access

## Deployment Steps

### Step 1: Go to Railway Dashboard
1. Open https://railway.app in your browser
2. Sign in with GitHub (easiest option)
3. Click **New Project**

### Step 2: Connect GitHub Repository
1. Click **Deploy from GitHub**
2. Select **GitHub** as the source
3. Find your repository: `team-task-manager`
4. Click **Deploy** to connect

Railway will detect your `Procfile` and `requirements.txt` automatically.

### Step 3: Add MySQL Database Service
1. In your Railway project, click **Add Service**
2. Search for and select **MySQL**
3. Railway will provision a MySQL instance
4. **Automatically adds**: `DATABASE_URL` environment variable

**Railway will set:**
- `DATABASE_URL=mysql+pymysql://user:pass@host:port/railway`

### Step 4: Configure Environment Variables

Click **Variables** in your Railway project dashboard and add these:

| Variable | Value | Example |
|----------|-------|---------|
| `SECRET_KEY` | Strong random string (32+ chars) | `k7#9@mP!x2$dQ8vN%5&wL3*jH4bR6tF1` |
| `CORS_ORIGINS` | Your Railway app URL | `https://team-task-manager-prod.railway.app` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration (minutes) | `60` |
| `CREATE_TABLES_ON_STARTUP` | Auto-create tables | `true` |

#### Getting Your Railway URL
After deployment, Railway gives you a public URL like:
```
https://[project-name]-[random].railway.app
```

Copy this URL and use it for `CORS_ORIGINS`:
```
CORS_ORIGINS=https://[project-name]-[random].railway.app
```

### Step 5: Deploy!

**Option A: Automatic Deployment (Recommended)**
- Railway automatically deploys when you push to GitHub `main` branch
- Just do: `git push origin main`
- Watch logs in Railway dashboard

**Option B: Manual Deploy via CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your Railway project
railway link

# Deploy
railway up
```

### Step 6: Verify Deployment

1. Click your app in Railway dashboard
2. Check the **Deployments** tab - should show "✓ Success"
3. Click the public URL in your Railway project
4. You should see the login page! 🎉

**View live logs:**
- In Railway dashboard: Click **Logs** tab
- Watch for: `Application startup complete`

## Environment Variables Explained

### Required Variables

**`DATABASE_URL`** (Auto-set by Railway MySQL)
```
mysql+pymysql://user:password@host:port/database
```
- Set by Railway MySQL plugin
- Do NOT manually set

**`SECRET_KEY`**
- Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Keep this SECURE - never commit to GitHub
- Change if you suspect it's compromised

### Important Variables

**`CORS_ORIGINS`**
- Set to your Railway app URL
- Without this, frontend can't reach backend
- Format: `https://your-app-name.railway.app` (NO trailing slash)

**`ACCESS_TOKEN_EXPIRE_MINUTES`**
- JWT token expiration (default: 60 minutes)
- Recommended: 60-120 minutes

**`CREATE_TABLES_ON_STARTUP`**
- Auto-create database tables on startup
- Set to `true` for first deployment
- Can set to `false` after successful deployment

## Troubleshooting

### ❌ Deployment Failed
1. Check **Logs** in Railway dashboard
2. Look for Python errors or missing dependencies
3. Verify all requirements are in `requirements.txt`
4. Check `Procfile` syntax

### ❌ Database Connection Error
1. Verify MySQL service is added
2. Check `DATABASE_URL` is set (should be auto-set)
3. Ensure `CREATE_TABLES_ON_STARTUP=true`
4. Check logs for connection string errors

### ❌ Frontend Can't Reach Backend
1. Verify `CORS_ORIGINS` includes your Railway URL
2. Check frontend API calls point to your Railway URL (not localhost)
3. Clear browser cache and localStorage

### ❌ Static Files Not Showing
1. Verify FastAPI serving static files from `app/static/`
2. Check Railway app is using correct Python path
3. Verify `Procfile` matches your `app/main.py` location

## Testing Your Deployment

### 1. Test Frontend
```
https://your-railway-url.railway.app/
```
Should show login page

### 2. Test Backend
```
https://your-railway-url.railway.app/healthz
```
Should return:
```json
{"status": "ok"}
```

### 3. Test API
```
curl -X POST https://your-railway-url.railway.app/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

## Monitoring

### Check Deployment Status
1. Go to Railway dashboard
2. Click your project
3. View **Deployments** tab
4. Green checkmark = success ✅

### View Live Logs
1. Railway dashboard → **Logs** tab
2. Select date range and refresh
3. Search for errors or warnings

### Monitor Performance
- Railway dashboard shows CPU, memory, and network usage
- Free tier has generous limits

## Scaling & Costs

- **Free tier:** Perfect for development/testing
- **Pro tier:** For production apps (pay as you go)
- Railway auto-scales if you exceed free limits
- No setup fees, only pay for usage

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Test all features on live app
3. ✅ Share URL with team
4. ✅ Set up monitoring/alerts (optional)
5. ✅ Update frontend to use production URL

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Report any problems

---

**Happy Deploying! 🚀**
