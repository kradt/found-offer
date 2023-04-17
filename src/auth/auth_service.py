from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database import models


def find_user_by_email(email: str) -> models.User:
	user = models.User.objects(email=email)
	print(user)
	if user:
		return user.get()
	else:
		return False


def create_user(email: str, password: str) -> models.User:
	user = models.User(email=email, password=password).save()
	return user
