import os
import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object("config.DevConfig")

api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
mail = Mail(app)

Migrate(app, db)

if not os.path.exists('logs'):
    os.makedirs('logs')
logging.config.fileConfig("logging.conf")
logger = logging.getLogger("menulis_ulasan")
