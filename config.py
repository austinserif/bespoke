"""Flask config file"""
import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """base app configuration class"""

    SECRET_KEY = os.environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class Development(Config):
    """configuration class for development and testing"""

    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class Production(Config):
    """configuration class for full production"""

    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI')

class Testing(Config):
    """configuration class for production testing"""

    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI')
    WTF_CSRF_ENABLED = False

