import unittest
from faker import Faker

from tests.main import app
from app.constants import PAYMENT_STATUSES
from app.utils import generate_hash, remove_null_attrs, get_request_origin, get_request_api_key, \
    get_json_request, calculate_score, clear_cpf


class TestUtils(unittest.TestCase):
    faker = Faker(["pt_BR"])

    http_origin = "http://localhost/"
    http_api_key = "0257b93f1b0028821160683259f8c524def75954f2ffaca3f391222fbc08cb30"

    def test_generate_hash(self):
        assert isinstance(generate_hash(self.faker.word()), str)

    def test_remove_null_attrs(self):
        params = {
            "param_one": "",
            "param_two": self.faker.word()
        }

        assert remove_null_attrs({**params, **{"param_three": None}}) == params

    def test_get_request_origin(self):
        with app.test_request_context("", headers={"ORIGIN": self.http_origin}):
            assert get_request_origin() == self.http_origin

    def test_get_request_api_key(self):
        with app.test_request_context("", headers={"API_KEY": self.http_api_key}):
            assert get_request_api_key() == self.http_api_key

    def test_get_json_request(self):
        data = {
            "param_one": str(self.faker.longitude()),
            "param_two": self.faker.word()
        }

        with app.test_request_context("", data=data):
            assert get_json_request() is not None

        with app.test_request_context("", data=data, content_type="application/json"):
            assert get_json_request() is not None

    def test_calculate_score(self):
        assert calculate_score(60, 0, PAYMENT_STATUSES) == 75
        assert calculate_score(18, 0, PAYMENT_STATUSES) == 100

    def test_clear_cpf(self):
        assert isinstance(int(clear_cpf(self.faker.cpf())), int)
