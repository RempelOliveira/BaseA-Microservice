from flask import request
from flask_restful import Resource, marshal

from app.utils import generate_hash, jwt_encode, get_request_authorization, clear_cpf
from app.decorators import tokenized, validate
from app.modules.users.repository import UserRepository
from app.modules.users.v1.serializers import UserSerializers


class User(Resource):
    @validate(UserSerializers.input_data())
    def post(self):
        data = request.data

        try:
            user = UserRepository.find_one({"cpf": clear_cpf(data["cpf"]), "password": generate_hash(data["password"])})

            if not user:
                return None, 401

        except Exception:
            return {"error": "internal server error"}, 500

        return marshal(user, UserSerializers.output_data()), 200, {"Authorization": jwt_encode(str(user.id))}

    @tokenized
    def delete(self):
        try:
            user = request.current_user
            user.unauthorized_tokens = (user.unauthorized_tokens or []) + [get_request_authorization()]

            UserRepository.update(user)

        except Exception:
            return {"error": "internal server error"}, 500

        return None, 204

    @tokenized
    def get(self):
        return marshal(request.current_user, UserSerializers.output_data(join_address=True)), 200
