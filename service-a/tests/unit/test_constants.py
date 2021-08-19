import unittest
from app.constants import DEBT_TYPES


class TestConstants(unittest.TestCase):
    def test_debt_types(self):
        assert type(DEBT_TYPES) == list
