import flask_login
import json
import requests
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from ..config import Config
from src import client
from src.auth import auth_service
from .tasks import send_message_to_email
from .forms import RegisterForm, LoginForm


auth_bp = Blueprint("auth_bp", template_folder="templates", static_folder="static", import_name=__name__)


def get_google_provider_cfg():
	return requests.get(Config.GOOGLE_DISCOVERY_URL).json()


# Google callback for get token that get account information
@auth_bp.route("/google-callback")
def google_callback():
	# Get authorization code Google sent back to you
	code = request.args.get("code")

	google_provider_cfg = get_google_provider_cfg()
	token_endpoint = google_provider_cfg["token_endpoint"]

	# Prepare all data that we need to have that get data for access to user information
	token_url, headers, body = client.prepare_token_request(
		token_endpoint,
		authorization_response=request.url,
		redirect_url=request.base_url,
		code=code
	)
	# Getting id_token, access_token, scopes
	token_response = requests.post(
		token_url,
		headers=headers,
		data=body,
		auth=(Config.CLIENT_ID, Config.CLIENT_SECRET),
	)

	# Parse the tokens!
	client.parse_request_body_response(json.dumps(token_response.json()))
	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]

	# Getting information about user
	uri, headers, body = client.add_token(userinfo_endpoint)
	userinfo_response = requests.get(uri, headers=headers, data=body).json()

	if userinfo_response.get("email_verified"):
		users_email = userinfo_response["email"]
	else:
		return "User email not available or not verified by Google.", 400

	user = auth_service.create_user(email=users_email, confirmed=True)
	if not user:
		user = auth_service.find_user_by_email(email=users_email)
	flask_login.login_user(user)

	# Send user back to homepage
	return redirect(url_for("auth_bp.home_page"))


# Login user using Google OAuth
@auth_bp.route("/google-login")
def google_login():
	google_provider_cfg = get_google_provider_cfg()
	authorization_endpoint = google_provider_cfg["authorization_endpoint"]

	# Get URL for Google authorization page
	request_uri = client.prepare_request_uri(
		authorization_endpoint,
		redirect_uri=request.root_url[:-1] + url_for("auth_bp.google_callback"),
		scope=["openid", "email", "profile"],
	)
	return redirect(request_uri)


# Confirm mail using token from url
@auth_bp.route("/confirm/<token>")
def confirm_email(token):
	email = auth_service.confirm_token(token)
	user = auth_service.find_user_by_email(email=email)
	if user:
		user.update(confirmed=True)
	return redirect(url_for(".home_page"))


# Login user in system from login form
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = auth_service.find_user_by_email(form.email.data)
		if user and user.check_password(form.password.data):
			flask_login.login_user(user, remember=form.remember_me.data)
			return redirect(url_for(".home_page"))
		else:
			flash("Wrong email or password")

	return render_template("login.html", form=form)


# Register user and send message to email for confirm account
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = auth_service.create_user(form.email.data, form.password.data)
		if not user:
			flash("User with this email already exist")
		else:
			token = auth_service.generate_confirmation_token(user.email)
			flask_login.login_user(user)
			send_data = {
				"sender": current_app.config["MAIL_DEFAULT_SENDER"],
				"recipients": [user.email],
			}
			confirm_link = url_for(".confirm_email", token=token, _external=True)
			send_message_to_email.delay(send_data, confirm_link)

			return redirect(url_for(".home_page"))
	return render_template("register.html", form=form)


# User log out route
@auth_bp.route("/logout")
@flask_login.login_required
def logout():
	flask_login.logout_user()
	return redirect(url_for("root_bp.index"))



@auth_bp.route("/me")
@flask_login.login_required
def recover_password():
	pass

# User Home page after login
@auth_bp.route("/me")
@flask_login.login_required
def home_page():
	return render_template("home.html", user=flask_login.current_user)
