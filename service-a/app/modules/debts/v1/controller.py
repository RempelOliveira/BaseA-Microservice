from flask import request
from flask_restful import Resource, marshal

from app.decorators import log, tokenized, validate
from app.modules.debts.repository import DebtRepository
from app.modules.debts.v1.serializers import DebtsSerializers


class Debts(Resource):
    @tokenized
    @validate(DebtsSerializers.input_args())
    @log
    def get(self):
        try:
            debts = DebtRepository.find(
                {"user_id": request.current_user.id}, request.pagination_args)

        except Exception:
            return {"error": "internal server error"}, 500

        return marshal(debts, DebtsSerializers.output_data()), 200
