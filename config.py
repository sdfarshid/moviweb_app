import os
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = os.getenv("DB_NAME", 'data/moviwebapp.sqlite')




SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, DB_NAME)}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"timeout": 15}}
