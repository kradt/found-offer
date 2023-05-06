import datetime

from bson import ObjectId
from mongoengine import ObjectIdField
from werkzeug.security import check_password_hash
from flask_login import UserMixin

from src import db, login_manager


class VacancySearchPattern(db.EmbeddedDocument):
	id = ObjectIdField(
		required=True,
		default=ObjectId,
		unique=True,
		primary_key=True,
		sparse=True)
	title = db.StringField()
	city = db.StringField()
	salary = db.FloatField()
	start_search = db.DateTimeField(default=datetime.datetime.now())


class User(db.Document, UserMixin):
	email = db.StringField(unique=True)
	password = db.StringField()
	confirmed = db.BooleanField(default=False)
	auto_search = db.ListField(db.EmbeddedDocumentField(VacancySearchPattern))

	def check_password(self, password) -> bool:
		return True if check_password_hash(self.password, password) else False

	def __repr__(self) -> str:
		return f"User {self.email}"


class Vacancy(db.Document):
	title = db.StringField(required=True)
	city = db.StringField()
	salary_from = db.FloatField()
	salary_to = db.FloatField()
	time_publish = db.DateTimeField()
	company = db.StringField()
	description = db.StringField()
	link = db.StringField()
	user_id = db.ObjectIdField()

	def __repr__(self):
		return f"<Vacancy {self.title}>"


@login_manager.user_loader
def load_user(user_id):
	return User.objects(id=user_id).get()
