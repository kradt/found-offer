from flask import Blueprint, render_template


auth_bp = Blueprint("auth_bp", template_folder="templates", static_folder="static", import_name=__name__)


@auth_bp.route("/login")
def login():
	return render_template("base.html")


@auth_bp.route("/register")
def register():
	return "Hello no name"


@auth_bp.route("/logout")
def logout():
	return "Bye"


@auth_bp.route("/me")
def home_page():
	return "my home"