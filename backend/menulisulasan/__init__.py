import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object("config.Config")

api = Api(app)
jwt = JWTManager(app)

db = SQLAlchemy(app)
Migrate(app, db)
