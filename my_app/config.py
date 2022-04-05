"""Flask config class."""
from pathlib import Path
import os


class Config(object):
    """ Sets the Flask base configuration that is common to all environments. """
    SECRET_KEY = 'q44II1qxOHIiuDobNoLLPQ'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                              str(Path(__file__).parent.joinpath('my_example.sqlite'))
    TESTING = False
    UPLOADED_PHOTOS_DEST = Path(__file__).parent.joinpath("static/img")
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    ADMINS = ['zcecjp0@gmail.com']


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True
