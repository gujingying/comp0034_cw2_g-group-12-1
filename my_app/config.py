"""Flask config class."""
from pathlib import Path


class Config(object):
    """ Sets the Flask base configuration that is common to all environments. """
    SECRET_KEY = 'q44II1qxOHIiuDobNoLLPQ'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(__file__).parent.joinpath('my_example.sqlite'))
    TESTING = False
    DATA_PATH = Path(__file__).parent.parent.joinpath("data")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True