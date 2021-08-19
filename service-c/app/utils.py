import os
import re
import json
import hashlib
from flask import request

from app.regular_expressions import NUMBERS_ONLY


def generate_hash(string):
    hash = hashlib.new(os.environ["HASH_ALGORITHM"])
    hash.update(bytes(str(string) + os.environ["HASH_SECRET"], encoding="utf-8"))

    return hash.hexdigest()


def remove_null_attrs(data):
    return {k: v for k, v in data.items() if v is not None}


def get_request_api_key():
    if request:
        api_key = request.headers.environ.get("HTTP_API_KEY", "")

    return api_key or None


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
