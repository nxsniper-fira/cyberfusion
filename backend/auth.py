from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, current_user
from models import User
from app import db, login_manager

auth_bp = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if user and user.check_password(data.get("password")) and user.active:
        login_user(user)
        session.permanent = True
        return jsonify({"success": True, "role": user.role})
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"success": True})

@auth_bp.route("/me", methods=["GET"])
def me():
    if not current_user.is_authenticated:
        return jsonify({"loggedIn": False}), 401
    return jsonify({
        "loggedIn": True,
        "username": current_user.username,
        "role": current_user.role,
    })