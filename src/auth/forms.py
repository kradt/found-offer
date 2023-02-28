from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class RegisterForm(FlaskForm):
	email = StringField("Email", validators=[Length(min=5, max=100), Email(), DataRequired()])
	password = PasswordField("Password", validators=[Length(min=8, max=100), EqualTo('confirm_password', "Passwords must be equal"), DataRequired()])
	confirm_password = PasswordField("Confirm", validators=[Length(min=8, max=100), DataRequired()])
	submit = SubmitField("Register")