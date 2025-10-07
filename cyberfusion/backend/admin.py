from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import User, Tool, AuditLog
from app import db

admin_bp = Blueprint("admin", __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated

@admin_bp.route("/users", methods=["GET"])
@login_required
@admin_required
def list_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "role": u.role,
        "active": u.active
    } for u in users])

@admin_bp.route("/users", methods=["POST"])
@login_required
@admin_required
def add_user():
    data = request.json
    user = User(username=data["username"], role=data.get("role", "whitehat"))
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"success": True})

@admin_bp.route("/users/<int:user_id>", methods=["PATCH"])
@login_required
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    if "role" in data:
        user.role = data["role"]
    if "active" in data:
        user.active = data["active"]
    db.session.commit()
    return jsonify({"success": True})

@admin_bp.route("/audit", methods=["GET"])
@login_required
@admin_required
def get_audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
    return jsonify([
        {
            "id": log.id,
            "user": log.user,
            "tool": log.tool,
            "timestamp": log.timestamp,
            "action": log.action,
            "details": log.details,
        } for log in logs
    ])