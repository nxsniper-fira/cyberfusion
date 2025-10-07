from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Tool, AuditLog
from app import db
import subprocess
from rbac import roles_required

tools_bp = Blueprint("tools", __name__)

CATEGORY_ROLES = {
    "whitehat": ["whitehat", "admin"],
    "blueteam": ["blueteam", "admin"],
    "redteam": ["redteam", "admin"],
    "grayhat": ["grayhat", "admin"],
    "blackhat": ["blackhat", "admin"],  # restrict as needed
}

@tools_bp.route("/", methods=["GET"])
@login_required
def list_tools():
    tools = Tool.query.all()
    return jsonify([{
        "id": tool.id,
        "name": tool.name,
        "description": tool.description,
        "category": tool.category,
        "status": tool.status
    } for tool in tools])

@tools_bp.route("/launch/<int:tool_id>", methods=["POST"])
@login_required
def launch_tool(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    allowed_roles = CATEGORY_ROLES.get(tool.category, ["admin"])
    if current_user.role not in allowed_roles:
        return jsonify({"success": False, "error": "You do not have permission to launch this tool."}), 403
    try:
        subprocess.Popen(tool.run_cmd, shell=True, cwd="/tools")
        log = AuditLog(user=current_user.username, tool=tool.name, action="launch", details="Launched via web")
        db.session.add(log)
        db.session.commit()
        return jsonify({"success": True, "message": f"Launched {tool.name}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500