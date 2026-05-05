# Quick Start - Team Task Manager on Railway

## 1️⃣ Fork the Repository
```bash
# Fork this repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/team-task-manager.git
cd team-task-manager
```

## 2️⃣ Deploy to Railway
```bash
# Option A: Using Railway Dashboard
# 1. Go to https://railway.app/dashboard
# 2. Click "New Project"
# 3. Select "Deploy from GitHub"
# 4. Choose this repository
# 5. Click "Deploy"

# Option B: Using Railway CLI
npm install -g @railway/cli
railway login
railway init --name team-task-manager
```

## 3️⃣ Configure Environment
Railway will prompt you to set environment variables. Minimum required:

```env
SECRET_KEY=your-generated-secret-key-here
CORS_ORIGINS=https://yourdomain.com
CREATE_TABLES_ON_STARTUP=true
```

## 4️⃣ Add Database
In Railway Dashboard → Your Project:
1. Click "New"
2. Select "Database" → "MySQL"
3. Railway auto-sets `DATABASE_URL`

## 5️⃣ Deploy & Access
1. Wait for build to complete (2-5 minutes)
2. Click "View Logs" to monitor startup
3. Get your URL from "Deploy" tab
4. Open `https://<your-railway-url>/` in browser

## ✅ Verify Deployment
```bash
# Check health endpoint
curl https://<your-railway-url>/healthz

# Should return:
# {"status": "ok"}
```

## 🔒 First-Time Setup

### Create Admin Account
In Railway Dashboard, add to environment variables:
```env
ADMIN_NAME=Admin User
ADMIN_EMAIL=admin@yourcompany.com
ADMIN_PASSWORD=change-this-password
```

Then redeploy. After logging in, **remove these variables** to prevent re-initialization.

### Update CORS
Update `CORS_ORIGINS` to your frontend URL:
```env
CORS_ORIGINS=https://app.yourdomain.com
```

## 📱 Test the App

1. **Register**: Open app and create account
2. **Login**: Sign in with created credentials
3. **Create Task**: Add a task from dashboard
4. **View Stats**: Check dashboard for task counts

## 🚀 Production Tips

| Setting | Local | Production |
|---------|-------|-----------|
| `CREATE_TABLES_ON_STARTUP` | true | false |
| `SECRET_KEY` | any string | long random value |
| `CORS_ORIGINS` | localhost | your domain |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 60 | 1440 (24h) |

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check "Build" tab logs in Railway |
| Database error | Wait 2 min after MySQL added, refresh |
| CORS error | Update `CORS_ORIGINS` to include your domain |
| 502 error | Check app logs, verify `$PORT` usage |
| Slow startup | Normal on Railway (30-60s cold start) |

## 📚 Resources

- [Railway Docs](https://docs.railway.app)
- [FastAPI Guide](https://fastapi.tiangolo.com)
- [Security Guide](./SECURITY.md)
- [Deployment Guide](./DEPLOYMENT.md)

## 🎯 Next Steps

- [ ] Deploy to Railway
- [ ] Add custom domain
- [ ] Set up monitoring
- [ ] Configure CI/CD
- [ ] Add API documentation (`/docs` endpoint)
- [ ] Enable email notifications
