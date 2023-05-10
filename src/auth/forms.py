from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# Form for register user
class RegisterForm(FlaskForm):
	email = StringField(
		"Email",
		validators=[Length(min=5, max=100), Email(), DataRequired()],
		render_kw={"placeholder": "Enter email"}
	)
	password = PasswordField(
		"Password",
		validators=[Length(min=8, max=100), DataRequired()],
		render_kw={"placeholder": "Enter password"}
	)
	confirm_password = PasswordField(
		"Confirm",
		validators=[Length(min=8, max=100), DataRequired(), EqualTo('password', "Passwords must be equal")],
		render_kw={"placeholder": "Confirm password"}
	)
	submit = SubmitField("Register")


# Form for login user
class LoginForm(FlaskForm):
	email = StringField(
		"Email",
		validators=[Length(min=5, max=100), Email(), DataRequired()],
		render_kw={"placeholder": "Enter email"}
	)
	password = PasswordField(
		"Password",
		validators=[Length(min=8, max=100), DataRequired()],
		render_kw={"placeholder": "Enter password"}
	)
	remember_me = BooleanField("Remember me?")
	submit = SubmitField("Log In")


# Form for confirm that user can recover password
class RecoverPasswordForm(FlaskForm):
	email = StringField(
		"Email",
		validators=[Length(min=5, max=100), Email(), DataRequired()],
		render_kw={"placeholder": "Enter email"}
	)
	code = StringField(
		"Code",
		validators=[Length(min=6, max=6)],
		render_kw={"placeholder": "Enter code"}
	)
	submit = SubmitField("Reset Password")
	send_code = StringField("Send Code")


# Form for write new user password
class NewPasswordForm(FlaskForm):
	password = PasswordField(
		"Password",
		validators=[Length(min=8, max=100), DataRequired()],
		render_kw={"placeholder": "Enter Password"}
	)
	confirm_password = PasswordField(
		"Repeat Password",
		validators=[Length(min=8, max=100), EqualTo('password', "Passwords must be equal"), DataRequired()],
		render_kw={"placeholder": "Enter Password Again"}
	)
	submit = SubmitField("Reset Password")
