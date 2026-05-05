# Security Implementation Summary

Team Task Manager implements comprehensive JWT-based authentication and role-based access control (RBAC) across all API endpoints.

## Implementation Details

### 1. JWT Authentication (OAuth2 Bearer)
- **Location**: `app/core/security.py` and `app/core/deps.py`
- **Algorithm**: HS256 with configurable secret key
- **Token Payload**: 
  - `sub` (subject) - user email
  - `exp` (expiration) - configurable via ACCESS_TOKEN_EXPIRE_MINUTES
  - `role` - user role (ADMIN or MEMBER)
- **Validation**: 
  - Signature verification against SECRET_KEY
  - Email lookup in database to confirm user exists and is active
  - 401 Unauthorized on invalid/expired tokens

### 2. Role-Based Access Control (RBAC)
- **Roles**: UserRole enum with ADMIN and MEMBER
- **Decorator**: `require_roles(*allowed_roles)` in `app/core/deps.py`
- **Enforcement Points**:
  - Route-level via FastAPI dependencies
  - Conditional logic in route handlers for nuanced permissions

### 3. Admin-Only Routes
All project and task creation/deletion restricted to ADMIN role:

```
ADMIN: can create, read, update, delete all projects
ADMIN: can assign tasks, delete tasks, create tasks
ADMIN: can view all task statistics
ADMIN: can manage team members
```

**Protected Routes**:
- `POST /projects` (create project)
- `GET /projects` (list projects)
- `GET /projects/{id}` (read project)
- `PUT /projects/{id}` (update project)
- `DELETE /projects/{id}` (delete project)
- `POST /projects/{id}/members` (add member)
- `DELETE /projects/{id}/members/{uid}` (remove member)
- `POST /tasks` (create task)
- `DELETE /tasks/{id}` (delete task)

### 4. Member-Only Restrictions
Members have limited write access:

```
MEMBER: can view only assigned tasks
MEMBER: can update task status only (read-only on other fields)
MEMBER: cannot create, delete, or manage projects
MEMBER: cannot assign tasks or manage team members
MEMBER: can view statistics for only their assigned tasks
```

**Member Access Logic**:
- GET /tasks - filtered to `assigned_to_id == current_user.id`
- GET /tasks/{id} - only if `assigned_to_id == current_user.id`
- PUT /tasks/{id} - status field only, 403 if trying other fields
- GET /tasks/dashboard/stats - counts only for assigned tasks

### 5. Error Handling
- `401 Unauthorized` - Missing or invalid JWT token
- `403 Forbidden` - Valid token but insufficient role/access
- `404 Not Found` - Resource doesn't exist or not accessible

### 6. Frontend Security
- JWT stored in localStorage (accessible to JavaScript)
- Token sent in Authorization header: `Bearer <token>`
- Pages redirect unauthenticated users to login
- Frontend restricts admin-only pages for members (server also enforces)

## Security Checklist

✓ JWT authentication on all protected routes
✓ SECRET_KEY required for token signing (configurable via .env)
✓ Token expiration implemented (configurable via .env)
✓ ADMIN role restricts project management
✓ ADMIN role restricts task creation/deletion
✓ ADMIN role can assign tasks
✓ MEMBER role can only view assigned tasks
✓ MEMBER role can only update task status
✓ MEMBER role cannot access projects
✓ Password hashing with bcrypt (verify_password)
✓ Active user check (is_active flag)
✓ CORS headers configured
✓ Security headers middleware
✓ Email validation on signup
✓ Unique email constraint in database

## Testing Security

### As Admin:
```bash
# Login as admin
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"change-me-now"}'

# Create project (works)
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Project","team_member_ids":[]}'

# View all tasks
curl http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer <token>"
```

### As Member:
```bash
# Login as member
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"member@example.com","password":"password123"}'

# Try to create project (403 Forbidden)
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Project","team_member_ids":[]}' 

# Try to delete task (403 Forbidden)
curl -X DELETE http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer <token>"

# Try to update task (works only for status field)
curl -X PUT http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status":"COMPLETED"}'

# Try to update other fields (403 Forbidden)
curl -X PUT http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Title"}'
```

## Future Enhancements

- API key authentication for service-to-service calls
- Refresh token rotation
- Rate limiting on auth endpoints
- Audit logging for sensitive operations
- Two-factor authentication (2FA)
- IP whitelisting for admin routes
- Password strength requirements
- Session management and logout token blacklist
