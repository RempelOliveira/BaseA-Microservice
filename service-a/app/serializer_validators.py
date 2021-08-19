import validate_cpf
from cerberus import Validator


class SerializerValidator(Validator):
    def cpf(value):
        if not validate_cpf.is_valid(value):
            raise ValueError("invalid")

        return value
