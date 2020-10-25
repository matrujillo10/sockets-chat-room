"""Configuration module"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))  # pylint: disable=invalid-name


class Config:
    """Config super class"""

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]


class ProductionConfig(Config):
    """Production configss"""

    DEBUG = False


class StagingConfig(Config):
    """Staging configss"""

    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """Dev configss"""

    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Test configss"""

    TESTING = True
