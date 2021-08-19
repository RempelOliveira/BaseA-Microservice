import random
import unittest

from faker import Faker
from unittest.mock import patch
from mongoengine.connection import _get_db

from tests.main import app, redis
from app.utils import generate_hash, clear_cpf
from app.constants import ORIGIN_TYPES, PAYMENT_METHODS
from app.modules.traces.repository import QueryRepository, TraceRepository, FinancialTransactionRepository
from app.modules.authorizations.repository import AuthorizationRepository


class TestConfig(unittest.TestCase):
    faker = Faker(["pt_BR"])
    traces_route = "/v1/users"

    def tearDown(self):
        _get_db().drop_collection("queries")
        _get_db().drop_collection("financial_transactions")
        _get_db().drop_collection("authorizations")

        redis.flushall()

    def query(self):
        query = QueryRepository(
            auth=self.authorization(),
            cpf=clear_cpf(self.faker.cpf()),
            datetime=self.faker.past_datetime()
        ).save()

        TraceRepository.save(f'{query.cpf}-last_query',
            {"origin": query.auth.request_origin.client, "datetime": str(query.datetime)})

        return query

    def financial_transaction(self):
        financial_transaction = FinancialTransactionRepository(
            auth=self.authorization(),
            cpf=clear_cpf(self.faker.cpf()),
            value=float(self.faker.pydecimal(left_digits=3, right_digits=2, positive=True)),
            method=PAYMENT_METHODS[2],
            datetime=self.faker.past_datetime()
        ).save()

        TraceRepository.save(f'{financial_transaction.cpf}-last_credit_card_purchase', {
            "value": financial_transaction.value,
            "origin": financial_transaction.auth.request_origin.client,
            "datetime": str(financial_transaction.datetime)
        })

        return financial_transaction

    def authorization(self):
        return AuthorizationRepository(
            api_key=generate_hash(self.faker.unix_time()),
            request_origin=dict(
                type=ORIGIN_TYPES[random.randint(0, len(ORIGIN_TYPES) - 1)],
                client=self.faker.company()
            )
        ).save()


class TestLastQuery(TestConfig):
    def test_post(self):
        auth = self.authorization()

        json_data = {
            "datetime": self.faker.past_datetime()
        }

        with patch("app.modules.traces.repository.redis", redis):
            last_query = app.test_client().post(
                f'{self.traces_route}/{self.faker.cpf()}/last_query', json=json_data)

            assert last_query.status_code == 401

            last_query = app.test_client().post(
                f'{self.traces_route}/{self.faker.cpf()}/last_query', json={}, headers={"API_KEY": auth.api_key})

            assert last_query.status_code == 422

            last_query = app.test_client().post(
                f'{self.traces_route}/{self.faker.cpf()}/last_query', json=json_data, headers={"API_KEY": auth.api_key})

            assert last_query.status_code == 201

        with patch("app.modules.traces.repository.redis", None):
            last_query = app.test_client().post(
                f'{self.traces_route}/{self.faker.cpf()}/last_query', json=json_data, headers={"API_KEY": auth.api_key})

        assert last_query.status_code == 500

    def test_get(self):
        with patch("app.modules.traces.repository.redis", redis):
            query = self.query()

            last_query = app.test_client().get(
                f'{self.traces_route}/{query.cpf}/last_query'
            )

            assert last_query.status_code == 401

            last_query = app.test_client().get(
                f'{self.traces_route}/{self.faker.cpf()}/last_query', headers={"API_KEY": query.auth.api_key}
            )

            assert last_query.status_code == 404

            last_query = app.test_client().get(
                f'{self.traces_route}/{query.cpf}/last_query', headers={"API_KEY": query.auth.api_key}
            )

            assert last_query.status_code == 200

        with patch("app.modules.traces.repository.redis", None):
            last_query = app.test_client().get(
                f'{self.traces_route}/{query.cpf}/last_query', headers={"API_KEY": query.auth.api_key}
            )

        assert last_query.status_code == 500


class TestLastCreditCardPurchase(TestConfig):
    def test_get(self):
        with patch("app.modules.traces.repository.redis", redis):
            purchase = self.financial_transaction()

            last_credit_card_purchase = app.test_client().get(
                f'{self.traces_route}/{purchase.cpf}/last_credit_card_purchase'
            )

            assert last_credit_card_purchase.status_code == 401

            last_credit_card_purchase = app.test_client().get(
                f'{self.traces_route}/{self.faker.cpf()}/last_credit_card_purchase', headers={
                    "API_KEY": purchase.auth.api_key})

            assert last_credit_card_purchase.status_code == 404

            last_credit_card_purchase = app.test_client().get(
                f'{self.traces_route}/{purchase.cpf}/last_credit_card_purchase', headers={
                    "API_KEY": purchase.auth.api_key})

            assert last_credit_card_purchase.status_code == 200

        with patch("app.modules.traces.repository.redis", None):
            last_credit_card_purchase = app.test_client().get(
                f'{self.traces_route}/{purchase.cpf}/last_credit_card_purchase', headers={
                    "API_KEY": purchase.auth.api_key})

        assert last_credit_card_purchase.status_code == 500


class TestFinancialTransactions(TestConfig):
    def test_get(self):
        with patch("app.modules.traces.repository.redis", redis):
            purchase = self.financial_transaction()

        financial_transactions = app.test_client().get(
            f'{self.traces_route}/{purchase.cpf}/financial_transactions'
        )

        assert financial_transactions.status_code == 401

        financial_transactions = app.test_client().get(
            f'{self.traces_route}/{self.faker.cpf()}/financial_transactions', headers={
                "API_KEY": purchase.auth.api_key})

        assert not financial_transactions.json["data"]
        assert financial_transactions.status_code == 200

        financial_transactions = app.test_client().get(
            f'{self.traces_route}/{purchase.cpf}/financial_transactions', headers={
                "API_KEY": purchase.auth.api_key})

        assert financial_transactions.json["data"]
        assert financial_transactions.status_code == 200

        query_string = {
            "page": 1, "per_page": 1
        }

        financial_transactions = app.test_client().get(
            f'{self.traces_route}/{purchase.cpf}/financial_transactions', query_string=query_string, headers={
                "API_KEY": purchase.auth.api_key})

        assert financial_transactions.json["data"]
        assert financial_transactions.status_code == 200

        with patch("app.modules.traces.repository.FinancialTransaction", None):
            financial_transactions = app.test_client().get(
                f'{self.traces_route}/{purchase.cpf}/financial_transactions', headers={
                    "API_KEY": purchase.auth.api_key})

        assert financial_transactions.status_code == 500
