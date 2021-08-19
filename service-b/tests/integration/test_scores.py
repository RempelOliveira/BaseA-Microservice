import random
import unittest

from faker import Faker
from unittest.mock import patch
from mongoengine.connection import _get_db

from tests.main import app
from app.utils import clear_cpf, generate_hash
from app.constants import ASSET_TYPES, PAYMENT_STATUSES, ORIGIN_TYPES
from app.modules.scores.repository import UserRepository
from app.modules.authorizations.repository import AuthorizationRepository


class TestScores(unittest.TestCase):
    faker = Faker(["pt_BR"])
    scores_route = "/v1/users"

    def tearDown(self):
        _get_db().drop_collection("users")
        _get_db().drop_collection("authorizations")

    def user(self):
        return UserRepository(
            age=random.randint(18, 75),
            cpf=clear_cpf(self.faker.cpf()),
            assets=[
                dict(
                    type=ASSET_TYPES[random.randint(0, len(ASSET_TYPES) - 1)],
                    payment_status=PAYMENT_STATUSES[random.randint(0, len(PAYMENT_STATUSES) - 1)]
                ) for i in range(random.randint(0, len(ASSET_TYPES) - 1))
            ]
        ).save()

    def authorization(self):
        return AuthorizationRepository(
            api_key=generate_hash(self.faker.unix_time()),
            request_origin=dict(
                type=ORIGIN_TYPES[random.randint(0, len(ORIGIN_TYPES) - 1)],
                client=self.faker.company()
            )
        ).save()

    def test_get(self):
        user = self.user()
        authorization = self.authorization()

        score = app.test_client().get(
            f'{self.scores_route}/{user.cpf}/score'
        )

        assert score.status_code == 401

        score = app.test_client().get(
            f'{self.scores_route}/{self.faker.cpf()}/score', headers={"API_KEY": authorization.api_key}
        )

        assert score.status_code == 404

        score = app.test_client().get(
            f'{self.scores_route}/{user.cpf}/score', headers={"API_KEY": authorization.api_key}
        )

        assert score.status_code == 200

        with patch("app.utils.PAYMENT_STATUSES", 1):
            score = app.test_client().get(
                f'{self.scores_route}/{user.cpf}/score', headers={"API_KEY": authorization.api_key}
            )

        assert score.status_code == 500
