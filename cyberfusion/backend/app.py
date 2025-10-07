from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "supersecretkey")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cyberfusion.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict'
)

CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
csrf = CSRFProtect(app)

from session_timeout import setup_session_timeout
setup_session_timeout(app, timeout_minutes=30)

from auth import auth_bp
from tools import tools_bp
from admin import admin_bp
from chat import chat_bp
from scheduler import scheduler_bp
from analytics import analytics_bp
from docs_api import docs_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(tools_bp, url_prefix="/api/tools")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(chat_bp, url_prefix="/api/chat")
app.register_blueprint(scheduler_bp, url_prefix="/api/scheduler")
app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
app.register_blueprint(docs_bp, url_prefix="/api/docs")

@app.route("/api/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.before_first_request
def setup():
    db.create_all()
    from models import User
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)