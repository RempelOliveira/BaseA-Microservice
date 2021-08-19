from app.modules.scores.model import User


class UserRepository:
    def __new__(self, **kwargs):
        return User(**kwargs)

    def find_one(args):
        return User.objects.get(**args)
