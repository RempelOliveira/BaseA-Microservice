from mongoengine import Document, EmbeddedDocument, \
    EmbeddedDocumentField, StringField, IntField, ListField

from app.constants import ASSET_TYPES, PAYMENT_STATUSES


class Asset(EmbeddedDocument):
    type = StringField(required=True, choices=ASSET_TYPES)
    payment_status = StringField(required=True, choices=PAYMENT_STATUSES)


class User(Document):
    age = IntField(required=True)
    cpf = StringField(required=True, unique=True)
    score = 0
    assets = ListField(EmbeddedDocumentField("Asset"))

    meta = {
        "collection": "users"
    }
