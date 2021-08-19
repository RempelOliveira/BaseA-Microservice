import random

from faker import Faker
from flask_seeder import Seeder

from app.constants import DEBT_TYPES
from app.utils import generate_hash, clear_cpf
from app.modules.users.repository import UserRepository
from app.modules.debts.repository import DebtRepository


class AddressesUsersAndDebtsSeeder(Seeder):
    def run(self):
        faker = Faker(["pt_BR"])
        cpfs = ["41090753004", "38028565034"] + [clear_cpf(faker.cpf()) for _ in range(3)]

        for i in range(1, 5):
            user = UserRepository(
                name=faker.name(),
                cpf=cpfs[i - 1],
                password=generate_hash("123456"),
                address=dict(
                    country=faker.current_country(),
                    state=faker.state(),
                    city=faker.city(),
                    street=faker.street_name(),
                    number=faker.building_number(),
                    postcode=faker.postcode()
                )
            )

            user.create()

            for _ in range(random.randint(5, 20)):
                DebtRepository(
                    type=DEBT_TYPES[random.randint(0, len(DEBT_TYPES) - 1)],
                    value=float(faker.pydecimal(left_digits=3, right_digits=2, positive=True)),
                    user_id=user.id
                ).create()
