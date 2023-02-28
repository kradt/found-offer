from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database import models


def find_user_by_email(db: Session, email: str) -> models.User:
	user = db.query(models.User).filter_by(email=email).first()
	if user:
		return user
	else:
		return False


def create_user(db: Session, email: str, password: str) -> models.User:
	user = models.User(email=email, password=password)
	try:
		db.add(user)
		db.commit()
		return user
	except IntegrityError as e:
		db.rollback()
		return False
