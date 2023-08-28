from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.widgets import NumberInput


class NewVacancyForm(FlaskForm):
    """
        Form for add new vacancy
    """
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(min=5, max=100)],
        render_kw={"placeholder": "Enter title"}
    )
    company = StringField(
        "Company",
        validators=[DataRequired(), Length(min=5, max=100)],
        render_kw={"placeholder": "Enter company name"}
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired(), Length(min=50, max=10000)],
        render_kw={"placeholder": "Enter description\nDo not forget to attach your contacts "}
    )
    city = StringField(
        "City",
        validators=[DataRequired(), Length(min=2, max=50)],
        render_kw={"placeholder": "Enter city"}
    )
    salary_from = IntegerField(
        "Salary from",
        widget=NumberInput(min=1000, max=1000000, step=100),
        render_kw={"placeholder": "Enter salary from"}
    )
    salary_to = IntegerField(
        "Salary to",
        widget=NumberInput(min=1000, max=1000000, step=100),
        render_kw={"placeholder": "Enter salary to"}
    )
    submit = SubmitField("Add Vacancy")

    def validate_salary_to(self, field):
        if field.data < self.salary_from.data:
            raise ValidationError("Salary to must be higher than salary from")


class AutoSearchForm(FlaskForm):
    """
        Form for add new auto search pattern
    """
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(min=5, max=100)],
        render_kw={"placeholder": "Enter title"}
    )
    city = StringField(
        "City",
        validators=[DataRequired(), Length(min=2, max=50)],
        render_kw={"placeholder": "Enter city"}
    )
    salary = IntegerField(
        "Salary to",
        widget=NumberInput(min=1000, max=1000000, step=100),
        render_kw={"placeholder": "Enter salary to"}
    )
    submit = SubmitField("Search Vacancy")
