import datetime
import math

from flask import Blueprint, render_template, jsonify, flash, request, Response
from src.database import models
from .forms import FilterForm
from ..parsing import engines

search_bp = Blueprint("search_bp", template_folder="templates", import_name=__name__)


@search_bp.route("/", methods=["GET"])
def find_work():
    form = FilterForm(request.args, meta={'csrf': False})
    parsed_request_args = "&".join(f"{arg}={request.args.get(arg)}" for arg in request.args)
    filter_dict = {}
    if form.title.data:
        filter_dict["title__icontains"] = form.title.data
    if form.city.data:
        filter_dict["city__icontains"] = form.city.data
    if form.salary_from.data:
        filter_dict["salary_from__gte"] = form.salary_from.data
    if form.salary_to.data:
        filter_dict["salary_to__lte"] = form.salary_to.data
    vacancies = models.Vacancy.objects(**filter_dict)
    if not vacancies:
        flash("Вибачте, але по вашому запиту ще немає вакансій")

    current_page = int(request.args.get("page", 1))
    items_per_page = 20
    offset = (current_page - 1) * items_per_page
    count_of_pages = math.floor(vacancies.count() / items_per_page)
    vacancies = vacancies.skip(offset).limit(items_per_page)
    return render_template(
        "search.html",
        form=form,
        vacancies=vacancies,
        current_page=current_page,
        count_of_pages=count_of_pages)


@search_bp.route("/offers/<job>", methods=["GET"])
def gtf(job):
    query = engines.WorkUA().get_page(job=job)
    return str(query.paginate(10, 1))
