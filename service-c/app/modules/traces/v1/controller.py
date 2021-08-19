from flask import request
from flask_restful import Resource, marshal

from app.decorators import tokenized, validate
from app.modules.traces.repository import TraceRepository, QueryRepository, FinancialTransactionRepository
from app.modules.traces.v1.serializers import TraceSerializers


class LastQuery(Resource):
    @tokenized
    @validate(TraceSerializers.query_input_data())
    def post(self, cpf):
        data = request.data

        data["cpf"] = cpf
        data["auth"] = request.current_external_api

        try:
            query = QueryRepository(**data)
            query.save()

            last_query = TraceRepository.save(f'{cpf}-last_query',
                {"origin": query.auth.request_origin.client, "datetime": str(query.datetime)})

        except Exception:
            return {"error": "internal server error"}, 500

        return marshal(last_query, TraceSerializers.query_output_data()), 201

    @tokenized
    def get(self, cpf):
        try:
            last_query = TraceRepository.find_one(f'{cpf}-last_query')

            if not last_query:
                return None, 404

        except Exception:
            return {"error": "internal server error"}, 500

        return marshal(last_query, TraceSerializers.query_output_data()), 200


class LastCreditCardPurchase(Resource):
    @tokenized
    def get(self, cpf):
        try:
            last_credit_card_purchase = TraceRepository.find_one(f'{cpf}-last_credit_card_purchase')

            if not last_credit_card_purchase:
                return None, 404

        except Exception:
            return {"error": "internal server error"}, 500

        return marshal(last_credit_card_purchase, TraceSerializers.credit_card_purchase_output_data()), 200


class FinancialTransactions(Resource):
    @tokenized
    @validate(TraceSerializers.financial_transactions_input_args())
    def get(self, cpf):
        try:
            financial_transactions = FinancialTransactionRepository.find_one(
                {"cpf": cpf}, request.pagination_args)

        except Exception:
            return {"error": "internal server error"}, 500

        return marshal(financial_transactions, TraceSerializers.financial_transactions_output_data()), 200
