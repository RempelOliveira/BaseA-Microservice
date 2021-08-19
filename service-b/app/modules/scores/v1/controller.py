from flask_restful import Resource, marshal
from mongoengine.errors import DoesNotExist

from app.decorators import tokenized
from app.utils import calculate_score
from app.modules.scores.repository import UserRepository
from app.modules.scores.v1.serializers import ScoreSerializers


class Score(Resource):
    @tokenized
    def get(self, cpf):
        try:
            user = UserRepository.find_one({"cpf": cpf})
            user.score = calculate_score(user.age, user.score, [asset.payment_status for asset in user.assets])

        except DoesNotExist:
            return None, 404
        except Exception:
            return {"error": "internal server error"}, 500

        return marshal(user, ScoreSerializers.output_data()), 200
