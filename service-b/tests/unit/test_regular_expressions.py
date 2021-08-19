import re
import unittest

from app.regular_expressions import NUMBERS_ONLY


class TestConstants(unittest.TestCase):
    def test_numbers_only(self):
        assert re.sub(NUMBERS_ONLY, "", "a1b2c3") == "123"
