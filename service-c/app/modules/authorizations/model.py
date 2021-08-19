from mongoengine import Document, EmbeddedDocument, \
    EmbeddedDocumentField, StringField

from app.constants import ORIGIN_TYPES


class RequestOrigin(EmbeddedDocument):
    type = StringField(required=True, choices=ORIGIN_TYPES)
    client = StringField(required=True, unique=True)


class Authorization(Document):
    api_key = StringField(required=True, unique=True)
    request_origin = EmbeddedDocumentField(RequestOrigin, required=True)

    meta = {
        "collection": "authorizations"
    }
