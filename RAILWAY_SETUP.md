# Railway Setup - Simple 3-Step Guide

Your app is now **bulletproof** for Railway! 🚀

## Step 1: Go to Railway Dashboard
```
https://railway.app
```

## Step 2: Select Your Project
- Find `team-task-manager` project
- Click it

## Step 3: Check MySQL Service
- Look for "mysql" service in the left sidebar
- If **NOT there**: Click **+ Add** → Search **MySQL** → Click it
- Wait 1 minute for MySQL to start

## Step 4: Deploy
- Click on "web" service (your app)
- Should auto-redeploy
- Watch **Deployments** tab - wait for green ✅
- If still red, check **Logs** tab for errors

## Step 5: Test
Go to:
```
https://web-production-9e620e.up.railway.app/
```

You should see **Login page** ✅

---

## If it Still Doesn't Work:

**Option 1: Restart Service**
- In Railway dashboard
- Click "web" service
- Click ⋮ menu
- Click **Restart**

**Option 2: Check Logs**
- Click **Logs** tab in "web" service
- Look for RED error messages
- Tell me what it says

**Option 3: Add Variables Manually**
- Click "web" service
- Go to **Variables** tab
- Click **+ Add**
- Add these 3:
  ```
  SECRET_KEY = anything-32-chars-or-more
  CORS_ORIGINS = *
  CREATE_TABLES_ON_STARTUP = true
  ```

That's it! 🎉
