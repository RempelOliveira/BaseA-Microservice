from app.modules.users.v1.controller import User
from app.modules.debts.v1.controller import Debts


def load_routes(api):
    api.add_resource(User,
        "/v1/users/login",
        "/v1/users/logout",
        "/v1/users/account")

    api.add_resource(Debts,
        "/v1/users/debts")
