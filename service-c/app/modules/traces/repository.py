import json

from app.db import redis
from app.modules.traces.model import Query, FinancialTransaction


class TraceRepository:
    def find_one(key):
        return json.loads(redis.get(key) or '[]')

    def save(key, data):
        redis.set(key, json.dumps(data))

        return data


class QueryRepository:
    def __new__(self, **kwargs):
        return Query(**kwargs)


class FinancialTransactionRepository:
    def __new__(self, **kwargs):
        return FinancialTransaction(**kwargs)

    def find_one(args, pagination=None):
        financial_transactions = FinancialTransaction.objects(**args) \
            .paginate(**pagination)

        return {
            "data": [financial_transaction for financial_transaction in financial_transactions.items], "pagination": {
                **pagination, **{"total": financial_transactions.total}}}
