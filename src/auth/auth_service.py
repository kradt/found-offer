from werkzeug.security import generate_password_hash

from src.database import models


def find_user_by_email(email: str) -> models.User | bool:
	user = models.User.objects(email=email)
	print(user)
	if user:
		return user.get()
	else:
		return False


def create_user(email: str, password: str) -> models.User:
	password_hash = generate_password_hash(password)
	user = models.User(email=email, password=password_hash).save()
	return user
