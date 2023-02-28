from flask import Blueprint, render_template


auth_bp = Blueprint("auth_bp", template_folder="templates", static_folder="static", import_name=__name__)


@auth_bp.route("/login")
def login():
	return render_template("login.html")


@auth_bp.route("/register")
def register():
	return render_template("register.html")


@auth_bp.route("/logout")
def logout():
	return "Bye"


@auth_bp.route("/me")
def home_page():
	return "my home"