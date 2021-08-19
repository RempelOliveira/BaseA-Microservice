from flask import request
from cerberus import Validator
from functools import wraps

from app.utils import remove_null_attrs, get_request_api_key, get_json_request
from app.modules.authorizations.repository import AuthorizationRepository


def tokenized(func=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            request.current_external_api = AuthorizationRepository.find_one(
                {"api_key": get_request_api_key()})

        except Exception:
            request.current_external_api = None

        if not request.current_external_api:
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
