from flask_login import current_user
from functools import wraps
from flask import jsonify

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                return jsonify({"error": "Insufficient privileges"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator