from flask import Blueprint, render_template, jsonify
from ..parsing import engines


search_bp = Blueprint("search_bp", template_folder="templates", import_name=__name__)


@search_bp.route("/")
def find_work():
	return render_template("search.html")


@search_bp.route("/offers/<job>", methods=["GET"])
def gtf(job):
	query = engines.WorkUA().get_page(job=job)
	return str(query.paginate(10, 1))
