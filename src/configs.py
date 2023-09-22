from dotenv import load_dotenv
from os import getenv


class Config:
    load_dotenv()
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI= getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False