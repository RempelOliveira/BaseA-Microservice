from sqlalchemy import not_
from sqlalchemy.orm import noload

from app.modules.users.model import db, User, Address


class UserRepository(User):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def create(self):
        if self.address:
            self.address = Address(**self.address)

        db.session.add(self)
        db.session.commit()

    def update(user):
        db.session.add(user)
        db.session.commit()

    def find_one(args):
        if args.get("not_"):
            return User.query.filter(User.id == args["id"],
                not_(User.unauthorized_tokens.any(args["not_"]["unauthorized_tokens"]))).first()

        return User.query.options(noload("address")).filter_by(**args).first()
