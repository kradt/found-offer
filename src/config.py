import secrets
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
	DEBUG = False
	SECRET_KEY = os.getenv("SECRET_KEY")
	SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
	PATH_TO_GOOGLE_CREDENTIALS = os.getcwd() + "/credentials.json"
	print(PATH_TO_GOOGLE_CREDENTIALS)
	MONGODB_SETTINGS = {
		"host": os.getenv("MONGO_URI")
	}
	