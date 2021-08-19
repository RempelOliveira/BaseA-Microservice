import random

from faker import Faker
from flask_seeder import Seeder

from app.utils import generate_hash, clear_cpf
from app.constants import ORIGIN_TYPES, PAYMENT_METHODS
from app.modules.authorizations.repository import AuthorizationRepository
from app.modules.traces.repository import TraceRepository, QueryRepository, FinancialTransactionRepository


class AuthorizationsAndTracesSeeder(Seeder):
    def run(self):
        faker = Faker(["pt_BR"])

        api_keys = ["c290ac1a33a665d0ceddf0b5cc0b5b6dcd1a8858a4ce7f0d8fbbd2427000dd1d", generate_hash(faker.unix_time())]
        authorizations = []

        for i in range(2):
            authorizations.append(
                AuthorizationRepository(
                    api_key=api_keys[i],
                    request_origin=dict(
                        type=ORIGIN_TYPES[i],
                        client=faker.company()
                    )
                ).save()
            )

        for i in range(random.randint(2, 20)):
            if i == 0:
                cpf = "41090753004"
            elif i == 1:
                cpf = "38028565034"
            else:
                cpf = clear_cpf(faker.cpf())

            datetimes = [faker.past_datetime() for _ in range(random.randint(10, 40))]

            query_datetimes = datetimes[:8]
            query_datetimes.sort()

            financial_transactions_datetimes = datetimes[8:]
            financial_transactions_datetimes.sort()

            for datetime in query_datetimes:
                query = QueryRepository(
                    auth=authorizations[random.randint(0, 1)],
                    cpf=cpf,
                    datetime=datetime
                ).save()

            credit_card_purchase = None

            for datetime in financial_transactions_datetimes:
                financial_transaction = FinancialTransactionRepository(
                    auth=authorizations[random.randint(0, 1)],
                    cpf=cpf,
                    value=float(faker.pydecimal(left_digits=3, right_digits=2, positive=True)),
                    method=PAYMENT_METHODS[random.randint(0, len(PAYMENT_METHODS) - 1)],
                    datetime=datetime
                ).save()

                if financial_transaction.method == PAYMENT_METHODS[1]:
                    credit_card_purchase = {
                        "value": financial_transaction.value,
                        "origin": query.auth.request_origin.client,
                        "datetime": str(financial_transaction.datetime)
                    }

            TraceRepository.save(f'{cpf}-last_query',
                {"origin": query.auth.request_origin.client, "datetime": str(query.datetime)})

            if credit_card_purchase:
                TraceRepository.save(f'{cpf}-last_credit_card_purchase', credit_card_purchase)
