class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False
    SECRET_KEY = "american-government-conspiracy"
    SQLALCHEMY_DATABASE_URI = "postgresql:///menulis_ulasan"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    TESTING = True
