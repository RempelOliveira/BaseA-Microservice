from flask_restful import fields


class ScoreSerializers:
    def output_data():
        return {
            "id": fields.String,
            "age": fields.Integer,
            "score": fields.Integer,
            "assets": fields.List(
                fields.Nested({
                    "type": fields.String,
                    "payment_status": fields.String
                })
            )
        }
