import os
from flask import Blueprint, jsonify, send_from_directory, request, abort, make_response
from flask_login import login_required, current_user

docs_bp = Blueprint("docs", __name__)
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")

@docs_bp.route("/", methods=["GET"])
@login_required
def list_docs():
    files = []
    for fname in os.listdir(DOCS_DIR):
        if fname.endswith(".md"):
            files.append(fname)
    return jsonify(files)

@docs_bp.route("/<filename>", methods=["GET"])
@login_required
def get_doc(filename):
    if not filename.endswith(".md") or "/" in filename or "\\" in filename:
        abort(400)
    path = os.path.join(DOCS_DIR, filename)
    if not os.path.isfile(path):
        abort(404)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Return as plain text
    resp = make_response(content)
    resp.mimetype = "text/plain"
    return resp

@docs_bp.route("/<filename>", methods=["POST"])
@login_required
def save_doc(filename):
    if current_user.role != "admin":
        abort(403)
    if not filename.endswith(".md") or "/" in filename or "\\" in filename:
        abort(400)
    content = request.json.get("content", "")
    with open(os.path.join(DOCS_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content)
    return jsonify({"success": True})