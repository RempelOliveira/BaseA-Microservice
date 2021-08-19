from app.modules.traces.v1.controller import LastQuery, LastCreditCardPurchase, FinancialTransactions


def load_routes(api):
    api.add_resource(LastQuery,
        "/v1/users/<string:cpf>/last_query")

    api.add_resource(LastCreditCardPurchase,
        "/v1/users/<string:cpf>/last_credit_card_purchase")

    api.add_resource(FinancialTransactions,
        "/v1/users/<string:cpf>/financial_transactions")
