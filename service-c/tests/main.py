from flask import Flask
from flask_restful import Api
from fakeredis import FakeStrictRedis

from app.db import db
from app.routes import load_routes

app = Flask(__name__)

app.config["TESTING"] = True
app.config["MONGODB_SETTINGS"] = {"host": "mongomock://localhost", "connect": False}

db.init_app(app)
redis = FakeStrictRedis()

load_routes(Api(app))
