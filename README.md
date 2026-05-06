# Team Task Manager 📋

A full-stack web application for managing team tasks and projects with role-based access control. Built with **FastAPI**, **MySQL**, **SQLAlchemy**, **JWT Authentication**, **Bootstrap 5**, and **Vanilla JavaScript**.

## 🎯 Features

- **User Authentication** - Register, login, forgot password with JWT tokens
- **Role-Based Access Control** - ADMIN and MEMBER roles with granular permissions
- **Task Management** - Create, read, update, delete tasks with status tracking
- **Project Management** - ADMIN-only project creation with team member management
- **Team Member Selection** - Add/remove team members by email lookup
- **Task Status Workflow** - Pending → In Progress → Completed → Overdue
- **Real-Time Dashboard** - Live task counts and statistics
- **Theme Toggle** - Dark mode 🌙 and light mode ☀️ with localStorage persistence
- **Responsive Design** - Bootstrap 5.3 for mobile and desktop
- **Secure API** - CORS headers, password hashing (bcrypt), JWT tokens (HS256)

## 🛠️ Tech Stack

- **Backend:** FastAPI 0.104+ (Python 3.11+)
- **Database:** MySQL 8.0 with SQLAlchemy ORM
- **Authentication:** python-jose (JWT), passlib (bcrypt)
- **Frontend:** Bootstrap 5.3, Vanilla JavaScript
- **Validation:** Pydantic v2
- **Security:** CORS middleware, security headers, password hashing

## 📋 Prerequisites

- Python 3.11+
- MySQL 8.0+
- pip (Python package manager)
- Git

## 🚀 Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/aayushpatidar07/team-task-manager.git
cd team-task-manager
```

### 2. Create Virtual Environment
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
# Application
APP_NAME=Team Task Manager
SECRET_KEY=your-super-secret-key-change-this-in-production

# Database
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/team_task_manager
# OR use individual variables:
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=team_task_manager

# Security
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Startup
CREATE_TABLES_ON_STARTUP=true
```

### 5. Create MySQL Database
```bash
mysql -u root -p
```
```sql
CREATE DATABASE team_task_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 6. Run the Application
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

Open your browser: **http://127.0.0.1:8001**

## 📚 API Endpoints

### Authentication (`/api/v1/auth`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Create new user account | ❌ |
| POST | `/login` | Login and receive JWT token | ❌ |
| GET | `/me` | Get current authenticated user | ✅ |
| GET | `/users` | List all users (ADMIN only) | ✅ |

### Tasks (`/api/v1/tasks`)
| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/` | Get user's tasks (ADMIN sees all) | ✅ | ADMIN, MEMBER |
| POST | `/` | Create new task | ✅ | ADMIN, MEMBER |
| PUT | `/{task_id}` | Update task | ✅ | ADMIN, MEMBER* |
| DELETE | `/{task_id}` | Delete task | ✅ | ADMIN |

*MEMBER can only update task status and their own tasks

### Projects (`/api/v1/projects`)
| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/` | Get all projects | ✅ | ADMIN |
| POST | `/` | Create new project | ✅ | ADMIN |
| PUT | `/{project_id}` | Update project | ✅ | ADMIN |
| DELETE | `/{project_id}` | Delete project | ✅ | ADMIN |
| POST | `/{project_id}/members` | Add team member | ✅ | ADMIN |
| DELETE | `/{project_id}/members` | Remove team member | ✅ | ADMIN |

## 🔐 Authentication Flow

1. **Register** - New users are created with MEMBER role by default
2. **Login** - Email and password validated, JWT token issued
3. **Token Usage** - Include `Authorization: Bearer <token>` in API requests
4. **Token Expiration** - Tokens expire after 60 minutes (configurable)

## 👥 User Roles

### ADMIN
- Create/edit/delete projects
- Manage team members
- View all tasks (across users)
- Delete any task
- Create and manage tasks
- Access user listing for member selection

### MEMBER
- Create tasks (auto-assigned to self)
- View own tasks only
- Update task status (Pending → In Progress → Completed → Overdue)
- Cannot create/delete other users' tasks
- Cannot access project management

## 🎨 UI Features

### Authentication Pages
- **Login** - Email/password with forgot password link
- **Register** - Create new account
- **Forgot Password** - Email validation with success message
- **Dashboard** - Real-time task statistics

### Task Management
- **Task Board** - Visual cards with status badges
- **Create Task** - Title, description, status, due date
- **Status Toggle** - Click to cycle through statuses
- **Delete Task** - With confirmation dialog

### Project Management (ADMIN only)
- **Create Project** - Set name and description
- **Add Members** - Search by email, add to team
- **Remove Members** - Click to remove from project
- **Edit Project** - Update name/description
- **Delete Project** - Remove entire project

### Theme Toggle
- **Dark Mode** (🌙) - Dark blue background, light text
- **Light Mode** (☀️) - Light background, dark text with teal accents
- **Persistence** - Theme choice saved in localStorage

## 🚢 Railway Deployment

### Prerequisites
- GitHub account with this repository
- Railway account (https://railway.app)
- Railway CLI installed (optional)

### Step 1: Connect GitHub Repository
1. Go to https://railway.app/dashboard
2. Click **New Project** → **Deploy from GitHub**
3. Select `aayushpatidar07/team-task-manager`
4. Authorize Railway to access your GitHub

### Step 2: Add MySQL Service
1. Click **Add Service** in your Railway project
2. Select **MySQL**
3. Railway automatically creates `DATABASE_URL` environment variable

### Step 3: Configure Environment Variables
In Railway project settings, add:
```
SECRET_KEY=your-production-secret-key
CORS_ORIGINS=https://[your-railway-url].railway.app
JWT_SECRET_KEY=another-secret-key-for-tokens
```

### Step 4: Deploy
1. Railway automatically detects `Procfile`:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
2. Deployment happens automatically on every push to `main` branch
3. View logs in Railway dashboard to confirm success

### Troubleshooting
- **Database connection fails**: Check `DATABASE_URL` is set correctly
- **Static files not loading**: Verify CORS_ORIGINS includes your Railway URL
- **Deployment stuck**: Check logs for Python dependency errors

## 📦 Project Structure

```
team-task-manager/
├── app/
│   ├── main.py                 # FastAPI app initialization
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── tasks.py        # Task CRUD operations
│   │       └── projects.py     # Project management
│   ├── crud/
│   │   ├── user.py             # User database operations
│   │   ├── task.py             # Task database operations
│   │   └── project.py          # Project database operations
│   ├── models/
│   │   ├── user.py             # User SQLAlchemy model
│   │   ├── task.py             # Task SQLAlchemy model
│   │   └── project.py          # Project SQLAlchemy model
│   ├── schemas/
│   │   ├── auth.py             # Authentication Pydantic schemas
│   │   ├── task.py             # Task Pydantic schemas
│   │   └── project.py          # Project Pydantic schemas
│   ├── core/
│   │   ├── config.py           # Settings and environment config
│   │   ├── database.py         # Database connection and session
│   │   └── security.py         # JWT and password utilities
│   └── static/
│       ├── index.html          # Main dashboard
│       ├── login.html          # Login page
│       ├── signup.html         # Registration page
│       ├── tasks.html          # Task board
│       ├── projects.html       # Project management (ADMIN)
│       ├── dashboard.html      # Statistics page
│       ├── css/
│       │   └── styles.css      # Dark/light theme styles
│       └── js/
│           └── app.js          # Frontend logic
├── scripts/
│   ├── test_api.py             # API integration tests
│   └── frontend_smoke.py       # Frontend smoke tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions CI/CD pipeline
├── requirements.txt            # Python dependencies
├── Procfile                    # Railway deployment configuration
├── .env.example                # Example environment variables
└── README.md                   # This file
```

## 🧪 Testing

### Run Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### API Integration Tests
```bash
python scripts/test_api.py
```

### Frontend Smoke Tests
```bash
python scripts/frontend_smoke.py
```

## 🔧 Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | Team Task Manager | Application display name |
| `SECRET_KEY` | change-me | JWT secret key (CHANGE IN PRODUCTION) |
| `DATABASE_URL` | - | MySQL connection string |
| `MYSQL_USER` | root | MySQL username |
| `MYSQL_PASSWORD` | - | MySQL password |
| `MYSQL_HOST` | 127.0.0.1 | MySQL host |
| `MYSQL_PORT` | 3306 | MySQL port |
| `MYSQL_DATABASE` | team_task_manager | Database name |
| `CORS_ORIGINS` | http://localhost:8000 | Allowed CORS origins |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 60 | JWT token expiration |
| `CREATE_TABLES_ON_STARTUP` | true | Auto-create database tables |

## 📝 Example Workflow

1. **Sign Up** → Create account (MEMBER role)
2. **Login** → Receive JWT token
3. **Create Task** → "Complete project documentation"
4. **View Dashboard** → See task statistics
5. **Update Task** → Mark as In Progress → Completed
6. **Toggle Theme** → Switch between dark/light mode
7. **Logout** → Token cleared from localStorage

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Aayush Patidar**
- GitHub: [@aayushpatidar07](https://github.com/aayushpatidar07)

## 🙏 Support

If you have any questions or issues, feel free to:
- Open an issue on GitHub
- Check existing documentation
- Review the API endpoint tables above

---

**Made with ❤️ for team productivity**