from flask import Blueprint, render_template
from .forms import RegisterForm


auth_bp = Blueprint("auth_bp", template_folder="templates", static_folder="static", import_name=__name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
	return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm()
	return render_template("register.html", form=form)


@auth_bp.route("/logout")
def logout():
	return "Bye"


@auth_bp.route("/me")
def home_page():
	return "my home"