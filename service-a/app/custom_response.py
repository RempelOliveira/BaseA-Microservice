import json
from flask import Response


class CustomResponse(Response):
    def __init__(self, response, **kwargs):
        response = response \
            if json.loads(response) else None

        return super(CustomResponse, self).__init__(response, **kwargs)
