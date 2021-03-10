import os


class Config:
    SECRET_KEY = "VeryVeryRandomStringForVeryVerySecurity"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FIRST_REGISTRATION = os.environ.get("FIRST_REGISTRATION")
