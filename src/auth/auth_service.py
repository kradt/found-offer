from werkzeug.security import generate_password_hash
from mongoengine.errors import NotUniqueError
from src.database import models


def find_user_by_email(email: str) -> models.User | bool:
	user = models.User.objects(email=email)
	if user:
		return user.get()
	else:
		return False


def create_user(email: str, password: str = None) -> models.User:
	if password:
		password = generate_password_hash(password)
	try:
		user = models.User(email=email, password=password).save()
		print(user)
	except NotUniqueError:
		user = None
	return user
