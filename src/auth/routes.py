from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import RegisterForm, LoginForm


auth_bp = Blueprint("auth_bp", template_folder="templates", static_folder="static", import_name=__name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		print(2)

	return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		print(1)
		return redirect(url_for(".login"))
	return render_template("register.html", form=form)


@auth_bp.route("/logout")
def logout():
	return "Bye"


@auth_bp.route("/me")
def home_page():
	return "my home"