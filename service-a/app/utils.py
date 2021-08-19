import os
import re
import jwt
import json
import hashlib

from flask import request
from datetime import datetime, timedelta

from app.regular_expressions import NUMBERS_ONLY


def jwt_encode(user_id):
    now = datetime.now()

    return "Bearer " + jwt.encode(
        {
            "iss": get_request_origin(),
            "sub": user_id,
            "iat": now.timestamp(),
            "exp": (now + timedelta(days=2)).timestamp()
        }, os.environ["JWT_SECRET"], algorithm=os.environ["JWT_ALGORITHM"]
    )


def jwt_decode(token):
    return jwt.decode(token,
        os.environ["JWT_SECRET"], os.environ["JWT_ALGORITHM"])


def generate_hash(string):
    hash = hashlib.new(os.environ["HASH_ALGORITHM"])
    hash.update(bytes(str(string) + os.environ["HASH_SECRET"], encoding="utf-8"))

    return hash.hexdigest()


def remove_null_attrs(data):
    return {k: v for k, v in data.items() if v is not None}


def get_request_origin():
    return request.environ.get("HTTP_ORIGIN", request.host_url)


def get_request_authorization():
    if request:
        token = request.headers.environ.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")

    return token or None


def get_json_request():
    def parse_json(data):
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    data[key] = json.loads(value, parse_int=str)
                except Exception:
                    pass

        return data

    def strip_attrs(json_data):
        if type(json_data) not in [str, dict]:
            return json_data

        data = {}

        for k, v in json_data.items():
            if isinstance(v, str):
                data[k] = v.strip() if v.strip() != "" else v
            else:
                data[k] = strip_attrs(v)

        return data

    if request.is_json:
        try:
            json_data = request.json
        except Exception:
            json_data = None
    else:
        json_data = parse_json(request.form.to_dict())

    return strip_attrs(json_data) or {}


def clear_cpf(cpf):
    return re.sub(NUMBERS_ONLY, "", cpf)
