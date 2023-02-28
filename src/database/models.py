from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from src import db, login_manager


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String)

	def __init__(self, email: str, password: str) -> None:
		self.email = email
		self.password = generate_password_hash(password)

	def check_password(self, password) -> bool:
		if check_password_hash(self.password, password):
			return True
		else:
			return False

	def __repr__(self) -> str:
		return f"User {self.email}"



@login_manager.user_loader
def load_user(user_id):
	return User.query.filter_by(id=user_id).first()


