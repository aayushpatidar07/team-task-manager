# 🚀 QUICK START - GitHub + Railway Deployment

## **In 5 Minutes: Copy-Paste These Commands**

---

### **Step 1: Create GitHub Repo (Browser)**

Go to **https://github.com/new** and fill:
- **Repository name:** `team-task-manager`
- **Visibility:** Public
- **Do NOT init with README**
- **Click Create**

---

### **Step 2: Push to GitHub (Terminal)**

Copy your GitHub username below, then run:

```powershell
# REPLACE "YOUR-USERNAME" with your actual GitHub username
git remote add origin https://github.com/YOUR-USERNAME/team-task-manager.git
git branch -M main
git push -u origin main
```

**Done! Your code is on GitHub ✅**

---

### **Step 3: Deploy to Railway**

1. **Go to https://railway.app**
2. **Sign up or login**
3. **Click: New Project → Deploy from GitHub**
4. **Select your `team-task-manager` repo**
5. **Wait for auto-detection, then click Deploy**

**Railway will:**
- Auto-detect your `Procfile` ✓
- Build your app ✓
- Give you a live URL ✓

---

### **Step 4: Add Environment Variables**

In Railway dashboard, go to **Variables** and add:

```
SECRET_KEY=your-generated-secret-key
DATABASE_URL=mysql+pymysql://user:pass@mysql:3306/team_task_manager
CORS_ORIGINS=https://YOUR-RAILWAY-URL.railway.app
CREATE_TABLES_ON_STARTUP=true
```

**How to get SECRET_KEY:**
```powershell
.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### **Step 5: Add MySQL Database**

In Railway dashboard:
1. **Create** → **MySQL**
2. Select **MySQL** from list
3. Railway auto-links it and provides connection string

---

### **Step 6: Verify It Works**

Once deployed, visit your live URL:
```
https://your-app-name.railway.app
```

- **Login page loads?** ✓
- **API docs working?** Check `/docs`
- **Health check?** Visit `/healthz` (should show `{"status":"ok"}`)

**Done! Your app is live! 🎉**

---

## **After Deployment: Record Demo Video**

Use this script (3–4 minutes):

```
[00:00] "This is Team Task Manager"
         - Show homepage/dashboard

[00:20] "Feature 1: Authentication"
         - Login with admin@example.com / Admin@12345

[00:40] "Feature 2: Create Project"
         - Go to Projects
         - Create new project
         - Add team members

[01:30] "Feature 3: Create & Track Tasks"
         - Go to Tasks
         - Create task with due date
         - Change status
         - Assign to member

[02:15] "Feature 4: Dashboard"
         - Show stats (Total, Completed, Pending, Overdue)

[02:45] "Tech Stack"
         - FastAPI, SQLAlchemy, MySQL, JWT, Bootstrap 5
         - Show API docs
         - Close
```

---

## **Submit These 3 Links:**

1. **Live URL:** `https://your-app.railway.app`
2. **GitHub:** `https://github.com/YOUR-USERNAME/team-task-manager`
3. **Demo Video:** `[YouTube/Loom Link]`

---

## **Common Issues?**

| Issue | Solution |
|-------|----------|
| `fatal: remote origin already exists` | Run: `git remote set-url origin https://...` |
| `Permission denied` on push | Run: `git config user.name "Your Name"` |
| Railway build fails | Check Railway logs → Check env variables |
| App crashes on Railway | Ensure `DATABASE_URL` and `SECRET_KEY` are set |

---

**Need help? See [SUBMISSION_GUIDE.md](./SUBMISSION_GUIDE.md) for detailed steps.**

**🎯 You're done in ~30 minutes! 🚀**
