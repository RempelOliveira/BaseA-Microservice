import os
import unittest
import requests_mock

from faker import Faker

from app.utils import clear_cpf
from app.services import Services


class TestServices(unittest.TestCase):
    faker = Faker(["pt_BR"])
    services = Services()

    @requests_mock.mock()
    def test_last_query(self, mock):
        cpf = self.faker.cpf()
        json_data = {
            "datetime": str(self.faker.past_datetime())
        }

        assert not self.services.last_query(
            cpf, json_data)

        mock.post(f'{os.environ.get("BASE_C_API")}/v1/users/{clear_cpf(cpf)}/last_query', status_code=201)

        last_query = self.services.last_query(
            cpf, json_data)

        assert last_query.status_code == 201
