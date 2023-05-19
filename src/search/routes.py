from flask import Blueprint, render_template, flash, request

from src.database import models
from .forms import FilterForm

search_bp = Blueprint("search_bp", template_folder="templates", import_name=__name__)


@search_bp.route("/", methods=["GET"])
def find_work():
    """
    Route for search vacancies
    """
    form = FilterForm(request.args, meta={'csrf': False})

    filter_dict = {}
    if form.title.data:
        filter_dict["title__icontains"] = form.title.data
    if form.city.data:
        filter_dict["city__icontains"] = form.city.data
    if form.salary_from.data:
        filter_dict["salary_from__gte"] = form.salary_from.data
    if form.salary_to.data:
        filter_dict["salary_to__lte"] = form.salary_to.data

    sort_value = "-time_publish"
    if request.args.get("sort_by") == '2':
        sort_value = "-salary_from"

    vacancies = models.Vacancy.objects(**filter_dict).order_by(sort_value)
    if not vacancies:
        flash("Вибачте, але по вашому запиту ще немає вакансій")

    current_page = int(request.args.get('page', 1))
    items_per_page = 20
    vacancies = vacancies.paginate(page=current_page, per_page=items_per_page)
    return render_template(
        "search.html",
        form=form,
        vacancies=vacancies)
