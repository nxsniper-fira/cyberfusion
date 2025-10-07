from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from models import AuditLog, Tool
from app import db

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/tool-usage", methods=["GET"])
@login_required
def tool_usage():
    # Admins see all; others see their own usage
    q = db.session.query(
        AuditLog.tool,
        func.count(AuditLog.id).label('count')
    )
    if current_user.role != "admin":
        q = q.filter(AuditLog.user == current_user.username)
    q = q.group_by(AuditLog.tool).order_by(func.count(AuditLog.id).desc())
    results = q.all()
    return jsonify([{"tool": r[0], "count": r[1]} for r in results])