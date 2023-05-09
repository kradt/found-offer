from functools import wraps
from flask import abort
import flask_login
from flask_mail import Message


def confirm_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = flask_login.current_user
        if user.confirmed:
            return func(*args, **kwargs)
        else:
            return abort(403, "Please confirm your account on mail")

    return wrapper


def make_message(message, send_data):
    msg = Message(
        message,
        sender=send_data["sender"],
        recipients=send_data["recipients"])
    return msg
