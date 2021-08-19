import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY
from sqlalchemy.dialects.postgresql import UUID

from app.db import db


class User(db.Model):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False)
    address = relationship("Address")
    name = Column(String(), nullable=False)
    cpf = Column(String(), nullable=False, unique=True)
    # email = Column(String(), nullable=False, unique=True)
    password = Column(String(), nullable=False)
    unauthorized_tokens = Column(ARRAY(String()), default=[])


class Address(db.Model):
    __tablename__ = "addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country = Column(String(), nullable=False)
    state = Column(String(), nullable=False)
    city = Column(String(), nullable=False)
    street = Column(String(), nullable=False)
    number = Column(String(), nullable=False)
    supplement = Column(String())
    postcode = Column(String(), nullable=False)
