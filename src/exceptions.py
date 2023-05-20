from flask import Blueprint, render_template

errors_bp = Blueprint("errors_bp", import_name=__name__)


@errors_bp.app_errorhandler(405)
def error_not_allowed(e):
    return render_template("error.html", error=e), 405


@errors_bp.app_errorhandler(404)
def error_not_found(e):
    return render_template("error.html", error=e), 404


@errors_bp.app_errorhandler(403)
def error_forbidden(e):
    return render_template("error.html", error=e), 403


@errors_bp.app_errorhandler(400)
def error_bad_request(e):
    return render_template("error.html", error=e), 400
