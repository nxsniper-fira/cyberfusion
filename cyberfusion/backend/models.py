from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False, default="whitehat")
    active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode("utf8")
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(32), nullable=False)
    install_cmd = db.Column(db.Text)
    run_cmd = db.Column(db.Text)
    status = db.Column(db.String(16), default="installed")

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), nullable=False)
    tool = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    action = db.Column(db.String(128))
    details = db.Column(db.Text)