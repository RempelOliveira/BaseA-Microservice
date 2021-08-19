import time
import random
import unittest
import requests_mock

from unittest.mock import patch
from faker import Faker

from tests.main import app, db
from app.utils import clear_cpf, generate_hash
from app.constants import DEBT_TYPES

from app.modules.users.model import Address, User
from app.modules.users.repository import UserRepository
from app.modules.debts.model import Debt
from app.modules.debts.repository import DebtRepository


class TestUser(unittest.TestCase):
    faker = Faker(["pt_BR"])
    users_route = "/v1/users"

    @classmethod
    def setUpClass(self):
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(self):
        with app.app_context():
            db.drop_all()

    def tearDown(self):
        with app.app_context():
            db.session.query(Debt).delete()
            db.session.query(User).delete()
            db.session.query(Address).delete()

            db.session.commit()

    def user(self, data):
        return UserRepository(
            name=self.faker.name(),
            cpf=clear_cpf(data["cpf"]),
            password=generate_hash(data["password"]),
            address=dict(
                country=self.faker.current_country(),
                state=self.faker.state(),
                city=self.faker.city(),
                street=self.faker.street_name(),
                number=self.faker.building_number(),
                postcode=self.faker.postcode()
            )
        )

    def debt(self, user):
        return DebtRepository(
            user_id=user.id,
            type=DEBT_TYPES[random.randint(0, len(DEBT_TYPES) - 1)],
            value=float(self.faker.pydecimal(left_digits=3, right_digits=2, positive=True))
        )

    @requests_mock.mock()
    def test_get(self, mock):
        debts = app.test_client().get(
            f'{self.users_route}/debts')

        assert debts.status_code == 401

        data = {
            "cpf": self.faker.cpf(),
            "password": self.faker.password(length=6)
        }

        with app.app_context():
            user = self.user(data)
            user.create()

            debt = self.debt(user)
            debt.create()

        login = app.test_client().post(
            f'{self.users_route}/login', json=data)

        debts = app.test_client().get(
            f'{self.users_route}/debts', headers={"Authorization": login.headers.get("Authorization")})

        assert debts.status_code == 200

        # sleeping to finish background service
        time.sleep(2)

        debts = app.test_client().get(
            f'{self.users_route}/debts', headers={"Authorization": self.faker.password()})

        assert debts.status_code == 401

        with patch("app.modules.debts.repository.Debt", None):
            debts = app.test_client().get(
                f'{self.users_route}/debts', headers={"Authorization": login.headers.get("Authorization")})

        assert debts.status_code == 500
