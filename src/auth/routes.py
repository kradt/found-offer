import flask_login
from flask import Blueprint, render_template, flash, redirect, url_for, current_app

from src import db
from src.auth import auth_service
from .forms import RegisterForm, LoginForm


auth_bp = Blueprint("auth_bp", template_folder="templates", static_folder="static", import_name=__name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = auth_service.find_user_by_email(db.session, form.email.data)
		if user and user.check_password(form.password.data):
			flask_login.login_user(user, remember=form.remember_me.data)
			return redirect(url_for(".home_page"))
		else:
			flash("Wrong email or password")

	return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = auth_service.create_user(db.session, form.email.data, form.password.data)
		if not user:
			flash("User with this email already exist")
		else:
			return redirect(url_for(".login"))
	return render_template("register.html", form=form)


@auth_bp.route("/logout")
@flask_login.login_required
def logout():
	flask_login.logout_user()
	return redirect(url_for("root_bp.index"))


@auth_bp.route("/me")
@flask_login.login_required
def home_page():
	return f"hello {flask_login.current_user.email}"