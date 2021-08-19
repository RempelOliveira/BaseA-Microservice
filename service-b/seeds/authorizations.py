from faker import Faker
from flask_seeder import Seeder

from app.utils import generate_hash
from app.constants import ORIGIN_TYPES
from app.modules.authorizations.repository import AuthorizationRepository


class AuthorizationsSeeder(Seeder):
    def run(self):
        faker = Faker(["pt_BR"])
        api_keys = ["c290ac1a33a665d0ceddf0b5cc0b5b6dcd1a8858a4ce7f0d8fbbd2427000dd1d", generate_hash(faker.unix_time())]

        for i in range(2):
            AuthorizationRepository(
                api_key=api_keys[i],
                request_origin=dict(
                    type=ORIGIN_TYPES[i],
                    client=faker.company()
                )
            ).save()
