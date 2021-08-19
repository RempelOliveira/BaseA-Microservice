import unittest
from app.constants import ORIGIN_TYPES, PAYMENT_METHODS


class TestConstants(unittest.TestCase):
    def test_origin_types(self):
        assert type(ORIGIN_TYPES) == list

    def test_payment_methods(self):
        assert type(PAYMENT_METHODS) == list
