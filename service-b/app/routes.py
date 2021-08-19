from app.modules.scores.v1.controller import Score


def load_routes(api):
    api.add_resource(Score,
        "/v1/users/<string:cpf>/score")
