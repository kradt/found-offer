from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from src import db, login_manager


class User(db.Document, UserMixin):
	email = db.StringField()
	password = db.StringField()

	def check_password(self, password) -> bool:
		return True if check_password_hash(self.password, password) else False

	def __repr__(self) -> str:
		return f"User {self.email}"


@login_manager.user_loader
def load_user(user_id):
	return User.objects(id=user_id).get()


