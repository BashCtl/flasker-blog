from dotenv import load_dotenv
from os import getenv
import os

class Config:
    load_dotenv()
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = f"{os.getcwd()}/src/static/images"

