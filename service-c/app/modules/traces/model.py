from flask_mongoengine import Document
from mongoengine import StringField, FloatField, DateTimeField, ReferenceField

from app.constants import PAYMENT_METHODS


class Query(Document):
    auth = ReferenceField("Authorization", required=True)
    cpf = StringField(required=True)
    datetime = DateTimeField(required=True)

    meta = {
        "collection": "queries"
    }


class FinancialTransaction(Document):
    auth = ReferenceField("Authorization", required=True)
    cpf = StringField(required=True)
    value = FloatField(required=True)
    method = StringField(required=True, choices=PAYMENT_METHODS)
    datetime = DateTimeField(required=True)

    meta = {
        "collection": "financial_transactions"
    }
