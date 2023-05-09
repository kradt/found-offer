import random
import flask_login
import json
import requests
from werkzeug.security import generate_password_hash
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, abort

from src.auth import forms
from src import client, redis_client
from src.utils import confirm_required
from src.auth import auth_service
from .tasks import send_message_to_email_for_confirm_him, send_code_to_email_for_reset_password


auth_bp = Blueprint("auth_bp", template_folder="templates", static_folder="static", import_name=__name__)


# Google callback for get token that get account information
@auth_bp.route("/google-callback")
def google_callback():
	# Get authorization code Google sent back to you
	code = request.args.get("code")
	token_endpoint = current_app.config["GOOGLE_TOKEN_ENDPOINT"]

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
		auth=(current_app.config["CLIENT_ID"], current_app.config["CLIENT_SECRET"]),
	)

	# Parse the tokens!
	client.parse_request_body_response(json.dumps(token_response.json()))
	userinfo_endpoint = current_app.config["GOOGLE_USER_INFO_ENDPOINT"]

	# Getting information about user
	uri, headers, body = client.add_token(userinfo_endpoint)
	userinfo_response = requests.get(uri, headers=headers, data=body).json()

	if userinfo_response.get("email_verified"):
		users_email = userinfo_response["email"]
	else:
		return abort(400, "User email not available or not verified by Google.")

	user = auth_service.create_user(email=users_email, confirmed=True)
	if not user:
		user = auth_service.find_user_by_email(email=users_email)
	flask_login.login_user(user)

	# Send user back to homepage
	return redirect(url_for("root_bp.home_page"))


# Login user using Google OAuth
@auth_bp.route("/google-login")
def google_login():
	authorization_endpoint = current_app.config["GOOGLE_AUTHORIZATION_ENDPOINT"]

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
	return redirect(url_for("root_bp.home_page"))


# Login user in system from login form
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		user = auth_service.find_user_by_email(form.email.data)
		if user and user.check_password(form.password.data):
			flask_login.login_user(user, remember=form.remember_me.data)
			return redirect(url_for("root_bp.home_page"))
		else:
			flash("Wrong email or password")

	return render_template("login.html", form=form)


# Register user and send message to email for confirm account
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
	form = forms.RegisterForm()
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
			send_message_to_email_for_confirm_him.delay(send_data, confirm_link)

			return redirect(url_for("root_bp.home_page"))
	return render_template("register.html", form=form)


# User log out route
@auth_bp.route("/logout")
@flask_login.login_required
def logout():
	flask_login.logout_user()
	return redirect(url_for("root_bp.index"))


# Reset password from user sent data
@auth_bp.route("/new-password", methods=["GET", "POST"])
@flask_login.login_required
@confirm_required
def write_new_password():
	form = forms.NewPasswordForm()
	if form.validate_on_submit():
		user = flask_login.current_user
		user.modify(password=generate_password_hash(form.password.data))
		return redirect(url_for("root_bp.home_page"))
	return render_template("new_password.html", form=form)


# Get user email and send code to mail for reset password
@auth_bp.route("/reset-password", methods=["GET", "POST"])
@flask_login.login_required
@confirm_required
def reset_password():
	form = forms.RecoverPasswordForm()
	email_was_sent = False
	if form.validate_on_submit():
		user = auth_service.find_user_by_email(email=form.email.data)
		if not user:
			flash("User with this email doesn't exist")
			return render_template("reset_password.html", form=form)
		if form.code.data:
			necessary_code = str(redis_client.get(user.email))
			if necessary_code and necessary_code == form.code.data:
				flask_login.login_user(user)
				return redirect(url_for(".write_new_password"))
			else:
				flash("Wrong code")
		code = random.randint(100000, 999999)
		redis_client.set(user.email, code, ex=3600)
		send_data = {
			"sender": current_app.config["MAIL_DEFAULT_SENDER"],
			"recipients": [user.email],
		}
		send_code_to_email_for_reset_password.delay(send_data, code)
		email_was_sent = True

	return render_template("reset_password.html", form=form, email_was_sent=email_was_sent)
