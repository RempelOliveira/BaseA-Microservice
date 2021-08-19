from flask_restful import reqparse, fields


class DebtsSerializers:
    def input_args():
        parser = reqparse.RequestParser()
        fields = [
            ("page", int, False, 1),
            ("per_page", int, False, 10)
        ]

        for field, type, required, value in fields:
            parser.add_argument(
                field, type=type, required=required, location="args", default=value)

        return parser

    def output_data():
        return {
            "data": fields.List(
                fields.Nested({
                    "id": fields.String,
                    "type": fields.String,
                    "value": fields.Float
                })
            ),
            "pagination": fields.Nested({
                "page": fields.Integer,
                "per_page": fields.Integer,
                "total": fields.Integer
            })
        }
