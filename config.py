import os
from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    POSTS_PER_PAGE = 16
    UPLOADS_DIRECTORY = os.path.join(
        os.path.dirname(__file__),
        'app',
        'static',
        'uploads',
        '',
    )

    ALLOWED_IMAGE_EXTENSIONS = ['JPEG', 'JPG', 'PNG', 'GIF']


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('PROD_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL')


class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get('DEV_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('P_DEV_DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')