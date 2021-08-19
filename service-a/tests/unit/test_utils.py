import uuid
import unittest

from faker import Faker

from tests.main import app
from app.utils import jwt_encode, jwt_decode, generate_hash, remove_null_attrs, get_request_origin, \
    get_request_authorization, get_json_request, clear_cpf


class TestUtils(unittest.TestCase):
    faker = Faker(["pt_BR"])
    http_origin = "http://localhost/"

    def test_jwt_encode(self):
        with app.test_request_context("", headers={"ORIGIN": self.http_origin}):
            assert "Bearer" in jwt_encode(str(uuid.uuid4()))

    def test_jwt_decode(self):
        user_id = str(uuid.uuid4())

        with app.test_request_context("", headers={"ORIGIN": self.http_origin}):
            jwt_token = jwt_encode(user_id)

        assert jwt_decode(jwt_token.replace("Bearer ", ""))["sub"] == user_id

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

    def test_get_request_authorization(self):
        user_id = str(uuid.uuid4())

        with app.test_request_context("", headers={"ORIGIN": self.http_origin}):
            jwt_token = jwt_encode(user_id)

        with app.test_request_context("", headers={"AUTHORIZATION": jwt_token}):
            assert get_request_authorization() == jwt_token.replace("Bearer ", "")

    def test_get_json_request(self):
        data = {
            "param_one": str(self.faker.longitude()),
            "param_two": self.faker.word()
        }

        with app.test_request_context("", data=data):
            assert get_json_request() is not None

        with app.test_request_context("", data=data, content_type="application/json"):
            assert get_json_request() is not None

    def test_clear_cpf(self):
        assert isinstance(int(clear_cpf(self.faker.cpf())), int)
