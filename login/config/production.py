import os

ADMINS = ['me@example.com']
DEBUG = False
SECRET_KEY = 'oh boy'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../data.sqlite3')
