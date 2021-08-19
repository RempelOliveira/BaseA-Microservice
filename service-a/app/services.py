import os
import requests

from app.utils import clear_cpf


class Services:
    base_c_api = os.environ.get("BASE_C_API")
    base_c_api_key = os.environ.get("BASE_C_API_KEY")

    def last_query(self, cpf, data):
        try:
            return requests.post(
                f'{self.base_c_api}/v1/users/{clear_cpf(cpf)}/last_query', json=data, headers={
                    "API-KEY": self.base_c_api_key})

        except Exception:
            pass

        return None
