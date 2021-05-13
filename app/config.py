import os
import distutils.util as conv

class Config:
    DEBUG = False
    SECRET_KEY = str(os.environ.get('SECRET_KEY'))
    SQLALCHEMY_DATABASE_URI = str(os.environ.get('DATABASE_URL'))
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_EXTENSIONS = list(str(os.environ.get('UPLOAD_EXTENTIONS')).split(' '))
    UPLOAD_PATH = str(os.environ.get('UPLOAD_IMAGE_PATH'))
    UPLOAD_DIR = str(os.environ.get('UPLOAD_IMAGE_DIR'))

    MAIL_SERVER = str(os.environ.get('MAIL_SERVER'))
    MAIL_PORT = str(os.environ.get('MAIL_PORT'))
    MAIL_USERNAME = str(os.environ.get('MAIL_USERNAME'))
    MAIL_PASSWORD = str(os.environ.get('MAIL_PASSWORD'))
    MAIL_USE_TLS = bool(conv.strtobool(str(os.environ.get('MAIL_USE_TLS'))))
    MAIL_USE_SSL = bool(conv.strtobool(str(os.environ.get('MAIL_USE_SSL'))))


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
