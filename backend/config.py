class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False
    # subject to change
    SECRET_KEY = "american-government-conspiracy"
    # subject to change
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:rahasiasekali@127.0.0.1:5432/menulis_ulasan"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    TESTING = True
