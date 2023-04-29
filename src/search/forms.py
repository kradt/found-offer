from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class FilterForm(FlaskForm):
    title = StringField("Title", render_kw={"placeholder": "Enter Job Title"})
    city = StringField("City", render_kw={"placeholder": "Enter Job location"})
    salary_from = StringField("Salary From", render_kw={"placeholder": "From"})
    salary_to = StringField("Salary To", render_kw={"placeholder": "To"})
    submit = SubmitField("Search")
