import os

from .database import DATABASE_URL, TEST_DATABASE_URL
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)


class Config(object):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
        'pool_size': 10,       # Number of connections to keep open inside the pool
        'max_overflow': 20    # Additional connections allowed above pool_sizef
    }
    REDIS_PASSWORD = '150000B6QKBfBDd489b63e05f81c31de6a69ab57de855ce781110919f65c076547fc27fbf1653e'
    # SESSION_REDIS_DB = 0




# Create the development config
class DevelopmentConfig(Config):
    DEBUG = bool(os.getenv('DEBUG', False))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT', 587)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = bool(os.getenv('MAIL_USE_TLS', True))
    MAIL_USE_SSL = bool(os.getenv('MAIL_USE_SSL', False))
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    


# Create the testing config
class TestingConfig(Config):
    DEBUG = False
    TESTING = True

    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')


# create the production config
class ProductionConfig(Config):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
