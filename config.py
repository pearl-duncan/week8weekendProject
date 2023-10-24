import os 

class Config:
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQULALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "shhh"
    JWT_TOKEN_LOCATION = ["headers"]