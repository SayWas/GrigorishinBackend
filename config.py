import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

AUTH_SECRET = os.getenv("AUTH_SECRET")
MANAGER_SECRET = os.getenv("MANAGER_SECRET")
RESET_SECRET = os.getenv("RESET_SECRET")
VERIFICATION_SECRET = os.getenv("VERIFICATION_SECRET")

EMAIL_LOGIN = os.getenv("EMAIL_LOGIN")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
