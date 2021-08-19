from flask_redis import FlaskRedis
from flask_mongoengine import MongoEngine
from flask_seeder import FlaskSeeder


db = MongoEngine()
redis = FlaskRedis()
seeder = FlaskSeeder()
