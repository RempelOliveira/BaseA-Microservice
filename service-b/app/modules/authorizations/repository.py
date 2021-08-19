from app.modules.authorizations.model import Authorization


class AuthorizationRepository:
    def __new__(self, **kwargs):
        return Authorization(**kwargs)

    def find_one(args):
        return Authorization.objects.get(**args)
