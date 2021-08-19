from flask import request
from cerberus import Validator
from functools import wraps
from datetime import datetime
from jwt import DecodeError, ExpiredSignatureError

from app.utils import jwt_decode, remove_null_attrs, get_request_authorization, get_json_request
from app.services import Services
from app.modules.users.repository import UserRepository

from multiprocessing import Process


def tokenized(func=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jwt_token = get_request_authorization()

        try:
            request.current_user = UserRepository.find_one(
                {"id": jwt_decode(jwt_token)["sub"], "not_": {"unauthorized_tokens": jwt_token}})

        except (DecodeError, ExpiredSignatureError):
            request.current_user = None

        if not request.current_user:
            return None, 401

        return func(*args, **kwargs)

    return wrapper


def validate(schema):
    def inner_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.method != "GET":
                data = get_json_request()
                validator = Validator(schema, purge_unknown=True)

                if not validator.validate(data):
                    return validator.errors, 422

                request.data = validator.normalized(data)

            else:
                request.args = remove_null_attrs(
                    schema.parse_args())

                request.pagination_args = {
                    "page": request.args["page"], "per_page": request.args["per_page"]
                }

                del request.args["page"]
                del request.args["per_page"]

            return func(*args, **kwargs)

        return wrapper
    return inner_function


def log(func=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def last_query():
            Services().last_query(
                request.current_user.cpf, {"datetime": str(datetime.utcnow())})

        process = Process(target=last_query)
        process.daemon = True

        process.start()

        return func(*args, **kwargs)

    return wrapper
