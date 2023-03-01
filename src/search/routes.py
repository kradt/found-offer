from flask import Blueprint, render_template


search_bp = Blueprint("search_bp", template_folder="templates", import_name=__name__)


@search_bp.route("/")
def find_work():
	return render_template("bases.html")