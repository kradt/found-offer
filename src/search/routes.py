from flask import Blueprint


search_bp = Blueprint("search_bp", template_folder="templates", import_name=__name__)


@search_bp.route("/")
def find_work():
	return "Work was finded"