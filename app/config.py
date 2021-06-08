import os
import distutils.util as conv

class Config:
    DEBUG = False
    SECRET_KEY = str(os.environ.get('SECRET_KEY'))
    SQLALCHEMY_DATABASE_URI = str(os.environ.get('DATABASE_URL'))
    ADMIN_PASSWORD = str(os.environ.get('ADMIN_PASSWORD'))
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_IMAGE_EXTENSIONS = list(str(os.environ.get('UPLOAD_IMAGE_EXTENSIONS')).split(' '))
    UPLOAD_IMAGE_PATH = str(os.environ.get('UPLOAD_IMAGE_PATH'))
    UPLOAD_IMAGE_DIR = str(os.environ.get('UPLOAD_IMAGE_DIR'))

    UPLOAD_DOC_EXTENSIONS = list(str(os.environ.get('UPLOAD_DOC_EXTENSIONS')).split(' '))
    UPLOAD_DOC_PATH = str(os.environ.get('UPLOAD_DOC_PATH'))
    UPLOAD_DOC_DIR = str(os.environ.get('UPLOAD_DOC_DIR'))

    MAIL_SERVER = str(os.environ.get('MAIL_SERVER'))
    MAIL_PORT = str(os.environ.get('MAIL_PORT'))
    MAIL_USERNAME = str(os.environ.get('MAIL_USERNAME'))
    MAIL_PASSWORD = str(os.environ.get('MAIL_PASSWORD'))
    MAIL_USE_TLS = bool(conv.strtobool(str(os.environ.get('MAIL_USE_TLS'))))
    MAIL_USE_SSL = bool(conv.strtobool(str(os.environ.get('MAIL_USE_SSL'))))

    VERIFY_URL = str(os.environ.get('VERIFY_URL'))


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
