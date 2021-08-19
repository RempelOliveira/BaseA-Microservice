import unittest
from app.constants import ASSET_TYPES, PAYMENT_STATUSES, ORIGIN_TYPES


class TestConstants(unittest.TestCase):
    def test_asset_types(self):
        assert type(ASSET_TYPES) == list

    def test_payment_statuses(self):
        assert type(PAYMENT_STATUSES) == list

    def test_origin_types(self):
        assert type(ORIGIN_TYPES) == list
