from flask import Blueprint, render_template


errors_bp = Blueprint("errors_bp", import_name=__name__)


@errors_bp.app_errorhandler(400)
@errors_bp.app_errorhandler(405)
@errors_bp.app_errorhandler(404)
def error(e):
    return render_template("error.html", error=e)
