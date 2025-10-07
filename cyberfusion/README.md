# CyberFusion – Secure LAN Cybersecurity Team Dashboard

CyberFusion is a secure, LAN-only dashboard for internal cybersecurity teams.  
It provides role-based dashboards, tool launching, chat, scheduling, analytics, and a local documentation portal.

## Quickstart

### Prerequisites
- Docker & Docker Compose
- (For local dev) Python 3.11+, Node.js 18+

### 1. Clone and Setup
```bash
git clone <your-repo-url> cyberfusion
cd cyberfusion
```

### 2. Generate Self-Signed SSL Certificate
```bash
mkdir -p nginx/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/certs/selfsigned.key \
  -out nginx/certs/selfsigned.crt \
  -subj "/CN=cyberfusion.local"
```

### 3. Run Everything
```bash
docker-compose up --build
```

### 4. Seed Tools
```bash
docker-compose exec backend python seed_tools.py
```

### 5. Access the Dashboard
- Go to: https://<your-LAN-IP>/
- Username: `admin`
- Password: `admin123` (change after first login!)

---

## LAN-only Security
- Nginx allows only LAN subnet (`192.168.1.0/24` by default; edit as needed)
- HTTPS enforced
- All actions audited, role-based RBAC

---

## Structure

```
cyberfusion/
├── backend/         # Flask API, docs, seeds, blueprints
├── frontend/        # React app
├── nginx/           # Nginx config, SSL
├── scripts/         # Backup/cleanup scripts
├── docker-compose.yml
├── README.md
```

---

## Admin Panel
- Manage users, roles, tools
- View audit logs
- Edit documentation

## Backups
```bash
./scripts/backup_db.sh
```

## For Developers
- Edit/add tools in `backend/seed_tools.py`, or via the admin panel
- Docs: add `.md` files to `backend/docs/`

---

## Security Checklist
- [x] Change all default passwords
- [x] Firewall: LAN-only access to ports 443/80
- [x] Regularly backup DB
- [x] Rotate logs
- [x] Review tool commands for safety