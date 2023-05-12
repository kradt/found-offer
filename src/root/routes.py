import flask_login
from flask import Blueprint, render_template, request, url_for, redirect, flash

from src.root import root_service
from src.root import forms
from src.utils import confirm_required


root_bp = Blueprint("root_bp", template_folder="templates", import_name=__name__)


# Index redirect to search route
@root_bp.route("/")
def index():
	return redirect(url_for("search_bp.find_work"))


# About route
@root_bp.route("/about")
def about():
	return render_template("base.html")


# User Home page after login
@root_bp.route("/me")
@flask_login.login_required
def home_page():
	user = flask_login.current_user
	patterns = user.auto_search
	current_page = int(request.args.get('page', 1))
	items_per_page = 5
	vacancies = root_service.get_user_vacancies(user.id).paginate(page=current_page, per_page=items_per_page)
	return render_template("home.html", vacancies=vacancies, user=user, patterns=patterns)


# Delete vacancy from user's vacancy list
@root_bp.route("/drop-vacancy/<vacancy_id>")
@flask_login.login_required
@confirm_required
def delete_vacancy(vacancy_id: str):
	vacancy = root_service.find_vacancy_by_id(vacancy_id=vacancy_id)
	vacancy.delete()
	return redirect(url_for(".home_page"))


# Delete search pattern from user's search patterns list
@root_bp.route("/drop-search-pattern/<pattern_id>", methods=["GET", "POST"])
@flask_login.login_required
@confirm_required
def delete_search_pattern(pattern_id):
	user = flask_login.current_user
	root_service.drop_pattern_from_user(user, pattern_id)
	return redirect(url_for(".home_page"))


# Route for add search pattern
@root_bp.route("/auto-search", methods=["GET", "POST"])
@flask_login.login_required
@confirm_required
def auto_search():
	form = forms.AutoSearchForm()
	if form.validate_on_submit():
		user = flask_login.current_user
		if len(user.auto_search) >= 3:
			flash("You can't have more than 3 search pattern")
		else:
			pattern = {"title": form.title.data, "city": form.city.data, "salary": float(form.salary.data)}
			root_service.add_auto_search_pattern_to_user(user, pattern)
			return redirect(url_for(".home_page"))

	return render_template("auto_search_vacancy.html", form=form)


# Route for add new vacancy
@root_bp.route("/new-vacancy", methods=["GET", "POST"])
@flask_login.login_required
@confirm_required
def add_new_vacancy():
	form = forms.NewVacancyForm()
	if form.validate_on_submit():
		# Here we can add Moderate vacancy
		user = flask_login.current_user
		vacancy = root_service.create_vacancy(
			title=form.title.data,
			company=form.company.data,
			city=form.city.data,
			description=form.description.data,
			salary_from=form.salary_from.data,
			salary_to=form.salary_to.data,
			user_id=user.id
		)
		if vacancy:
			return redirect(url_for(".home_page"))
		flash("Something went wrong, try again")
	return render_template("new_vacancy.html", form=form)
