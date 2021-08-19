import unittest

from unittest.mock import patch
from faker import Faker

from tests.main import app, db

from app.utils import clear_cpf, generate_hash
from app.modules.users.model import Address, User
from app.modules.users.repository import UserRepository


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

    def test_post(self):
        login = app.test_client().post(
            f'{self.users_route}/login', json={})

        assert login.status_code == 422

        login = app.test_client().post(
            f'{self.users_route}/login', json={"cpf": ""})

        assert login.status_code == 422

        data = {
            "cpf": self.faker.cpf(),
            "password": self.faker.password(length=6)
        }

        login = app.test_client().post(
            f'{self.users_route}/login', json=data)

        assert login.status_code == 401

        data = {
            "cpf": self.faker.cpf(),
            "password": self.faker.password(length=6)
        }

        with app.app_context():
            user = self.user(data)
            user.create()

        login = app.test_client().post(
            f'{self.users_route}/login', json=data)

        assert login.status_code == 200

        with patch("app.modules.users.repository.User", None):
            login = app.test_client().post(
                f'{self.users_route}/login', json=data)

        assert login.status_code == 500

    def test_delete(self):
        logout = app.test_client().delete(
            f'{self.users_route}/logout')

        assert logout.status_code == 401

        data = {
            "cpf": self.faker.cpf(),
            "password": self.faker.password(length=6)
        }

        with app.app_context():
            user = self.user(data)
            user.create()

        login = app.test_client().post(
            f'{self.users_route}/login', json=data)

        with patch("app.modules.users.repository.db", None):
            logout = app.test_client().delete(
                f'{self.users_route}/logout', headers={"Authorization": login.headers.get("Authorization")})

        assert logout.status_code == 500

        logout = app.test_client().delete(
            f'{self.users_route}/logout', headers={"Authorization": login.headers.get("Authorization")})

        assert logout.status_code == 204

        logout = app.test_client().delete(
            f'{self.users_route}/logout', headers={"Authorization": login.headers.get("Authorization")})

        assert logout.status_code == 401

    def test_get(self):
        account = app.test_client().get(
            f'{self.users_route}/account')

        assert account.status_code == 401

        data = {
            "cpf": self.faker.cpf(),
            "password": self.faker.password(length=6)
        }

        with app.app_context():
            user = self.user(data)
            user.create()

        login = app.test_client().post(
            f'{self.users_route}/login', json=data)

        account = app.test_client().get(
            f'{self.users_route}/account', headers={"Authorization": login.headers.get("Authorization")})

        assert account.status_code == 200

        account = app.test_client().get(
            f'{self.users_route}/account', headers={"Authorization": self.faker.password()})

        assert account.status_code == 401
