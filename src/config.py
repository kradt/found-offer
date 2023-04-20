import secrets
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

class Config:
	DEBUG = True
	SECRET_KEY = os.getenv("SECRET_KEY")
	SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
	MONGO_URI = os.getenv("MONGO_URI")
	MONGODB_SETTINGS = {
		'alias': 'default',
		"host": os.getenv("MONGO_URI")
	}
	