from functools import wraps
from flask import redirect, url_for, abort
import flask_login


def confirm_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = flask_login.current_user
        if user.confirmed:
            return func(*args, **kwargs)
        else:
            return abort(403, "Please confirm your account on mail")
    return wrapper
