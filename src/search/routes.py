from flask import Blueprint, render_template, jsonify
from src.database import models
from .forms import FilterForm
from ..parsing import engines


search_bp = Blueprint("search_bp", template_folder="templates", import_name=__name__)


@search_bp.route("/", methods=["GET", "POST"])
def find_work():
	form = FilterForm()
	vacancies = models.Vacancy.objects()[:50]
	if form.validate_on_submit():
		filter_dict = {}
		if form.title:
			filter_dict["title__icontains"] = form.title.data
		elif form.city:
			filter_dict["city__icontains"] = form.city.data
		elif form.salary_from:
			filter_dict["salary_from__gte"] = form.salary_from.data
		elif form.salary_to:
			filter_dict["salary_to__lte"] = form.salary_to.data
		vacancies = models.Vacancy.objects(**filter_dict)[:50]


	return render_template("search.html", form=form, vacancies=vacancies)


@search_bp.route("/offers/<job>", methods=["GET"])
def gtf(job):
	query = engines.WorkUA().get_page(job=job)
	return str(query.paginate(10, 1))
