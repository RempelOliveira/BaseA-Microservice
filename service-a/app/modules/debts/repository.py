from app.modules.debts.model import db, Debt


class DebtRepository(Debt):
    def __init__(self, **kwargs):
        super(Debt, self).__init__(**kwargs)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def find(args, pagination=None):
        debts = Debt.query.filter_by(**args).paginate(**pagination)

        return {
            "data": [debt for debt in debts.items], "pagination": {
                **pagination, **{"total": debts.total}}}
