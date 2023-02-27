from flask import Blueprint


auth_bp = Blueprint("auth_bp", template_folder="templates", import_name=__name__)


@auth_bp.route("/login")
def login():
	return "Hello my friend"


@auth_bp.route("/register")
def register():
	return "Hello no name"


@auth_bp.route("/logout")
def logout():
	return "Bye"


@auth_bp.route("/me")
def home_page():
	return "my home"