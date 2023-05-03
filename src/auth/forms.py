from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
	email = StringField("Email", validators=[Length(min=5, max=100), Email(), DataRequired()], render_kw={"placeholder":"Enter email"})
	password = PasswordField("Password", validators=[Length(min=8, max=100), DataRequired()], render_kw={"placeholder":"Enter password"})
	confirm_password = PasswordField("Confirm", validators=[Length(min=8, max=100), DataRequired(), EqualTo('password', "Passwords must be equal")],
					  					        render_kw={"placeholder":"Confirm password"})
	submit = SubmitField("Register")


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[Length(min=5, max=100), Email(), DataRequired()], render_kw={"placeholder":"Enter email"})
	password = PasswordField("Password", validators=[Length(min=8, max=100), DataRequired()], render_kw={"placeholder":"Enter password"})
	remember_me = BooleanField("Remember me?" )
	submit = SubmitField("Log In")


class RecoverPasswordEmail(FlaskForm):
	email = StringField("Email", validators=[Length(min=5, max=100), Email(), DataRequired()], render_kw={"placeholder": "Enter email"})
	submit = SubmitField("Get confirm code")

class RecoverPasswordCode(FlaskForm):
	code = StringField("Code", validators=[Length(min=6, max=6), DataRequired()], render_kw={"placeholder": "Enter code"})
	submit = SubmitField("Reset Password")
