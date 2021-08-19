import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_migrate import Migrate

from app.db import db, seeder
from app.routes import load_routes
from app.custom_response import CustomResponse


app = Flask(__name__)

app.url_map.strict_slashes = False
app.response_class = CustomResponse

app.config["MONGODB_SETTINGS"] = {"host": f'{os.environ["DATABASE_URL"]}/{os.environ["DATABASE"]}', "connect": False}

db.init_app(app)
seeder.init_app(app, db)

CORS(app, resources={r"/*": {"origins": "*"}})
Migrate(app, db)

load_routes(Api(app))


@app.errorhandler(404)
def not_found(e):
    return {}, e.code


if __name__ == "__main__":
    app.run()
