# Team Task Manager - Final Submission Guide

## 📋 Overview

Your app is **100% complete** and ready for submission. Follow these 3 simple steps:

1. **Create GitHub Repository** (5 min)
2. **Deploy to Railway** (15 min)
3. **Record Demo Video** (10–15 min)

---

## **Step 1: Create GitHub Repository**

### Option A: Web Browser (Easiest)

1. **Go to GitHub.com** → Sign in (create account if needed)
2. **Click `+` → New Repository**
3. **Fill in details:**
   - **Repository name:** `team-task-manager`
   - **Description:** Task management app with role-based access (Admin/Member)
   - **Visibility:** Public
   - **Do NOT initialize with README** (we have one)
4. **Click `Create Repository`**

### Option B: GitHub CLI (If installed)

```powershell
gh repo create team-task-manager --public --source=. --push --remote=origin
```

---

## **Step 2: Push Code to GitHub**

After creating the repo on GitHub, run these commands in your terminal:

```powershell
# Add GitHub remote (replace YOUR-USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/team-task-manager.git

# Rename branch to main (GitHub default)
git branch -M main

# Push all commits to GitHub
git push -u origin main
```

**Expected output:**
```
Counting objects: 55, done.
Compressing objects: 100% (50/50), done.
Writing objects: 100% (55/55), ...
To https://github.com/YOUR-USERNAME/team-task-manager.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ **Your code is now on GitHub!**

---

## **Step 3: Deploy to Railway**

### Prerequisites

1. **GitHub account** (from Step 1)
2. **Railway.app account** - [Sign up free](https://railway.app)
3. **Code pushed to GitHub** (from Step 2)

### Deployment Steps

#### 3a. Connect Railway to GitHub

1. Go to **[railway.app](https://railway.app)** → Sign in
2. **New Project** → **Deploy from GitHub**
3. **Select your repository:** `team-task-manager`
4. **Authorize Railway** to access GitHub
5. **Select the repo** from the list

#### 3b. Configure Environment Variables

Railway will automatically detect your `Procfile`. Now add environment variables:

1. In Railway dashboard, go to **Variables**
2. **Add the following variables:**

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"` | Must be a long random string |
| `DATABASE_URL` | `mysql+pymysql://team_task_user:StrongPassword123!@mysql:3306/team_task_manager` | Railway MySQL host will be different |
| `CORS_ORIGINS` | `https://YOUR-APP-URL.railway.app` | Will get this after first deploy |
| `CREATE_TABLES_ON_STARTUP` | `true` | Auto-create tables on startup |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Session timeout |

**Important:** Railway provides MySQL. Get the connection string from Railway's MySQL plugin once added.

#### 3c. Add MySQL Database

1. In Railway dashboard → **Create** → **MySQL**
2. Select **MySQL** from the list
3. Railway will auto-link it and provide credentials
4. Copy the `MYSQL_URL` or individual credentials
5. Add to environment variables (Railway does this automatically)

#### 3d. Deploy

1. Click **Deploy** button
2. Railway builds and deploys automatically
3. **Watch the logs** for deployment status
4. Once complete, you'll see a **live URL** like:
   ```
   https://team-task-manager-prod.railway.app
   ```

#### 3e. Verify Deployment

Open your live URL in browser:
- **Dashboard:** `https://YOUR-URL.railway.app`
- **API Docs:** `https://YOUR-URL.railway.app/docs`
- **Health check:** `https://YOUR-URL.railway.app/healthz`

✅ **Your app is now live on Railway!**

---

## **Step 4: Record Demo Video (2–5 minutes)**

Use **OBS Studio** (free) or your laptop's screen recorder:

### Demo Flow (Follow this script):

**[0:00–0:20] Intro**
- "This is the Team Task Manager - a full-stack web app for project and task management"
- Show the live URL and homepage

**[0:20–1:00] Authentication**
- Show signup page
- Create a new account OR show login with demo account
- Demonstrate login with: `admin@example.com` / `Admin@12345`
- Show authenticated dashboard

**[1:00–2:00] Create Project (Admin)**
- Click "Projects" (top menu)
- Create a new project: "Q2 Product Roadmap"
- Add team members: Select 2 members
- Save and show the created project

**[2:00–3:00] Create & Assign Tasks**
- Go to "Tasks"
- Create a task: "Design homepage mockups"
- Set status to "IN_PROGRESS"
- Set due date to tomorrow
- Assign to a team member
- Show task saved successfully

**[3:00–4:00] Dashboard**
- Go to Dashboard
- Show statistics: Total tasks, Completed, Pending, Overdue
- Click on a task to view details
- Show update task status

**[4:00–4:30] Closing**
- "Features demonstrated: User auth, role-based access, project management, task tracking, and dashboard analytics"
- "Tech stack: FastAPI, SQLAlchemy, MySQL, JWT, Bootstrap 5"
- Show API docs (`/docs`)

### Recording Tips

✅ **Do:**
- Clear and calm voice
- Click slowly so viewers can see
- Show URL in address bar
- Minimize terminal windows

❌ **Don't:**
- Show your real database password
- Share secret keys
- Record with too much speed

### Upload & Share

- **Upload to:** YouTube (unlisted), Loom, or included in submission
- **Share link** with your submission

---

## **Final Checklist Before Submission**

- [ ] GitHub repository created and public
- [ ] All 55 files committed and pushed
- [ ] Railway deployment successful (live URL works)
- [ ] All environment variables configured
- [ ] MySQL database connected
- [ ] Demo video recorded (2–5 min)
- [ ] README.md in repository
- [ ] DEPLOYMENT.md included
- [ ] `/docs` endpoint shows API documentation

---

## **Submission Details**

**Submit with:**

```
📌 Assignment: Team Task Manager

✅ Live URL: https://YOUR-APP-URL.railway.app
✅ GitHub Repo: https://github.com/YOUR-USERNAME/team-task-manager
✅ Demo Video: [YouTube Link / Loom Link]

📦 Features Delivered:
- ✓ User authentication (Signup/Login) with JWT
- ✓ Role-based access control (Admin/Member)
- ✓ Project creation and team management
- ✓ Task creation, assignment, and status tracking
- ✓ Dashboard with statistics (total, completed, pending, overdue)
- ✓ Responsive Bootstrap 5 UI
- ✓ REST API with full CRUD operations
- ✓ MySQL database with normalized schema
- ✓ Production-ready deployment on Railway
- ✓ Comprehensive documentation

⚙️ Tech Stack:
- Backend: FastAPI, SQLAlchemy, PyMySQL
- Frontend: Bootstrap 5, HTML, CSS, JavaScript (Fetch API)
- Database: MySQL 8.0+
- Authentication: JWT (python-jose)
- Password Hashing: bcrypt
- Deployment: Railway (PaaS)
```

---

## 🆘 **Troubleshooting**

### Push to GitHub fails
```powershell
# Check remote
git remote -v

# Update remote if wrong
git remote set-url origin https://github.com/YOUR-USERNAME/team-task-manager.git

# Try push again
git push -u origin main
```

### Railway deployment fails
1. Check **Build Logs** in Railway dashboard
2. Verify environment variables are set
3. Ensure `Procfile` is present in root
4. Check MySQL is properly linked

### App works locally but not on Railway
- Check `CORS_ORIGINS` includes your Railway URL
- Verify `DATABASE_URL` is correct (use Railway's MySQL credentials)
- Check logs: **Railway Dashboard → Logs**

---

## 📞 **Need Help?**

- **Railway Docs:** https://docs.railway.app
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **GitHub Help:** https://docs.github.com

---

**🎉 You're ready for submission! Good luck! 🚀**
