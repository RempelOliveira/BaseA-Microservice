import random

from faker import Faker
from flask_seeder import Seeder

from app.constants import ASSET_TYPES, PAYMENT_STATUSES
from app.utils import clear_cpf
from app.modules.scores.repository import UserRepository


class AssetsAndUsersSeeder(Seeder):
    def run(self):
        faker = Faker(["pt_BR"])
        cpfs = ["41090753004", "38028565034"] + [clear_cpf(faker.cpf()) for _ in range(3)]

        for i in range(5):
            UserRepository(
                age=random.randint(18, 75),
                cpf=cpfs[i],
                assets=[
                    dict(
                        type=ASSET_TYPES[random.randint(0, len(ASSET_TYPES) - 1)],
                        payment_status=PAYMENT_STATUSES[random.randint(0, len(PAYMENT_STATUSES) - 1)]
                    ) for i in range(random.randint(0, len(ASSET_TYPES) - 1))
                ]
            ).save()
