from flask_restful import reqparse, fields


class TraceSerializers:
    def query_input_data():
        return {
            "datetime": {
                "type": "string",
                "required": True
            }
        }

    def query_output_data():
        return {
            "origin": fields.String,
            "datetime": fields.String
        }

    def credit_card_purchase_output_data():
        return {
            "value": fields.Float,
            "origin": fields.String,
            "datetime": fields.String
        }

    def financial_transactions_input_args():
        parser = reqparse.RequestParser()
        fields = [
            ("page", int, False, 1),
            ("per_page", int, False, 10)
        ]

        for field, type, required, value in fields:
            parser.add_argument(
                field, type=type, required=required, location="args", default=value)

        return parser

    def financial_transactions_output_data():
        return {
            "data": fields.List(
                fields.Nested({
                    "value": fields.Float,
                    "method": fields.String,
                    "datetime": fields.String
                })
            ),
            "pagination": fields.Nested({
                "page": fields.Integer,
                "per_page": fields.Integer,
                "total": fields.Integer
            })
        }
