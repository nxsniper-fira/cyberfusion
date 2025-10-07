from app import db
from models import AuditLog
from datetime import datetime, timedelta

def cleanup_audit_logs(days=90):
    cutoff = datetime.utcnow() - timedelta(days=days)
    deleted = AuditLog.query.filter(AuditLog.timestamp < cutoff).delete()
    db.session.commit()
    print(f"Deleted {deleted} old audit log entries.")