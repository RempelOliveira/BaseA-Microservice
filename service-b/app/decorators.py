from functools import wraps

from app.utils import get_request_api_key
from app.modules.authorizations.repository import AuthorizationRepository


def tokenized(func=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            AuthorizationRepository.find_one({"api_key": get_request_api_key()})
        except Exception:
            return None, 401

        return func(*args, **kwargs)

    return wrapper
