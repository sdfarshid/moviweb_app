import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
