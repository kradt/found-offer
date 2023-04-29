from flask import Blueprint, render_template, jsonify

from .forms import FilterForm
from ..parsing import engines


search_bp = Blueprint("search_bp", template_folder="templates", import_name=__name__)


@search_bp.route("/", methods=["GET", "POST"])
def find_work():
	form = FilterForm()
	if form.validate_on_submit():
		pass

	return render_template("search.html", form=form)


@search_bp.route("/offers/<job>", methods=["GET"])
def gtf(job):
	query = engines.WorkUA().get_page(job=job)
	return str(query.paginate(10, 1))
