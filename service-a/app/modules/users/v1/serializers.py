from flask_restful import fields
from app.serializer_validators import SerializerValidator


class UserSerializers:
    def input_data():
        return {
            "cpf": {
                "type": "string",
                "coerce": SerializerValidator.cpf,
                "required": True
            },
            "password": {
                "type": "string",
                "minlength": 6,
                "required": True
            }
        }

    def output_data(join_address=False):
        output_data = {
            "id": fields.String,
            "name": fields.String,
            "cpf": fields.String
        }

        if join_address:
            output_data["address"] = fields.Nested({
                "street": fields.String,
                "number": fields.String,
                "supplement": fields.String,
                "postcode": fields.String,
                "country": fields.String,
                "state": fields.String,
                "city": fields.String
            })

        return output_data
