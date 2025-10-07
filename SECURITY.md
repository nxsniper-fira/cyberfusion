# CyberFusion Security Checklist

- [x] HTTPS enforced (self-signed certificate, Nginx proxy)
- [x] LAN-only access (Nginx `allow`/`deny` and local firewall)
- [x] Strong password hashing (bcrypt)
- [x] Session timeout with auto-logout
- [x] Secure cookies: `SESSION_COOKIE_SECURE`, `HTTPONLY`, `SAMESITE`
- [x] CSRF protection (Flask-WTF)
- [x] Role-based access control (RBAC)
- [x] Audit logs for all tool launches and admin actions
- [x] Tool command sandboxing (review all `run_cmd` entries)
- [x] SQLite backups and log rotation
- [x] No default passwords in production!
- [x] Run containers as non-root where possible