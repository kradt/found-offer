from flask_mail import Message
from functools import wraps
from flask import abort
import flask_login


def confirm_required(func):
    """
    Decorator checks if user is confirmed 
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = flask_login.current_user
        if user.confirmed:
            return func(*args, **kwargs)
        else:
            abort(403, "Please confirm your account on mail")

    return wrapper


def make_message(message, send_data):
    """
    Function for make message template for flask mail send
    """
    msg = Message(
        message,
        sender=send_data["sender"],
        recipients=send_data["recipients"])
    return msg
