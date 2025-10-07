from flask import session, redirect, url_for, request
from datetime import timedelta

def setup_session_timeout(app, timeout_minutes=30):
    app.permanent_session_lifetime = timedelta(minutes=timeout_minutes)

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        # Optionally, you can implement stricter timeout logic here

# Usage in app.py:
# from session_timeout import setup_session_timeout
# setup_session_timeout(app, timeout_minutes=30)