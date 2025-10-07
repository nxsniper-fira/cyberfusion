from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from threading import Thread
from time import sleep
from models import Tool, AuditLog
from app import db
from datetime import datetime
import subprocess

scheduler_bp = Blueprint("scheduler", __name__)

# In-memory scheduled jobs (for demonstration; for production use APScheduler or Celery)
SCHEDULED_JOBS = []

def run_scheduled_job(job):
    sleep(job["delay"] * 60)
    tool = Tool.query.get(job["tool_id"])
    if tool:
        try:
            subprocess.Popen(tool.run_cmd, shell=True, cwd="/tools")
            log = AuditLog(user=job["user"], tool=tool.name, action="scheduled_launch", details=f"Launched via scheduler at {datetime.utcnow().isoformat()}Z")
            db.session.add(log)
            db.session.commit()
        except Exception:
            pass

@scheduler_bp.route("/jobs", methods=["GET"])
@login_required
def list_jobs():
    # Only admin can see all jobs
    if current_user.role == "admin":
        return jsonify(SCHEDULED_JOBS)
    return jsonify([j for j in SCHEDULED_JOBS if j["user"] == current_user.username])

@scheduler_bp.route("/jobs", methods=["POST"])
@login_required
def schedule_job():
    data = request.json
    job = {
        "user": current_user.username,
        "tool_id": data["tool_id"],
        "delay": int(data.get("delay", 1)),  # minutes
        "created": datetime.utcnow().isoformat() + "Z",
    }
    SCHEDULED_JOBS.append(job)
    t = Thread(target=run_scheduled_job, args=(job,))
    t.daemon = True
    t.start()
    return jsonify({"success": True, "job": job})

# In app.py, register:
# from scheduler import scheduler_bp
# app.register_blueprint(scheduler_bp, url_prefix="/api/scheduler")