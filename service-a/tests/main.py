import os

from flask import Flask
from flask_restful import Api

from app.db import db
from app.routes import load_routes

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f'{os.environ["DATABASE_URL"]}/{os.environ["DATABASE"]}_tests'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

load_routes(Api(app))
