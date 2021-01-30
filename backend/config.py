class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False

    # SECRET, subject to change
    SECRET_KEY = "american-government-conspiracy"
    SECURITY_PASSWORD_SALT = "another-conspiracy"

    # DB and JWT, subject to change
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:rahasiasekali@127.0.0.1:5432/menulis_ulasan"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    # MAIL, subject to change
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = "menulisulasan.dev"
    MAIL_PASSWORD = "Rahasiakitabersama25"
    DEFAULT_MAIL_SENDER = "menulisulasan.dev@gmail.com"


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    TESTING = True
