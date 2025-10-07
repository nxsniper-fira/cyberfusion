```markdown
# CyberFusion Backend

## Quickstart

1. Create a Python virtual environment (optional for local dev):

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

2. Run the backend:

    python app.py

3. (To seed the database with tools)

    python seed_tools.py

## API Endpoints

- `/api/auth/login` (POST): Login with `{username, password}`
- `/api/auth/logout` (POST): Logout
- `/api/auth/me` (GET): Get current session info
- `/api/tools/` (GET): List all tools
- `/api/tools/launch/<id>` (POST): Launch a tool (RBAC enforced)
- `/api/admin/users` (GET, POST): List/add users (admin only)
- `/api/admin/users/<id>` (PATCH): Edit user (admin only)
- `/api/admin/audit` (GET): Audit logs (admin only)
```