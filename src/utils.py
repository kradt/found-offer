from functools import wraps
from flask import redirect, url_for
import flask_login


def confirm_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = flask_login.current_user
        if user.confirmed:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth_bp.home_page"))
    return wrapper
