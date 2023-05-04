from flask import Blueprint, render_template


root_bp = Blueprint("root_bp", template_folder="templates", import_name=__name__)


@root_bp.route("/")
def index():
	return render_template("base.html")
