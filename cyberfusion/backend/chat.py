from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from datetime import datetime

chat_bp = Blueprint("chat", __name__)

# Simple in-memory storage for demonstration; for production, use a DB table.
CHAT_HISTORY = []

@chat_bp.route("/messages", methods=["GET"])
@login_required
def get_messages():
    # Optionally, you can paginate or limit messages
    return jsonify(CHAT_HISTORY[-50:])  # Last 50 messages

@chat_bp.route("/messages", methods=["POST"])
@login_required
def post_message():
    data = request.json
    message = {
        "user": current_user.username,
        "role": current_user.role,
        "text": data.get("text", ""),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    CHAT_HISTORY.append(message)
    # Optional: persist to DB for audit
    return jsonify({"success": True, "message": message})

# In app.py, register:
# from chat import chat_bp
# app.register_blueprint(chat_bp, url_prefix="/api/chat")