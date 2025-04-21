import mercadopago
from dotenv import load_dotenv
import os

def realizar_pagamento(items):
    load_dotenv()

    sdk = mercadopago.SDK(f'{os.getenv("MP_ACCESS_TOKEN")}')

    request = {
        "items": items,
        "back_urls": {
            "success": "http://127.0.0.1:8000/carrinho/compra_realizada/",
            "failure": "http://127.0.0.1:8000/carrinho/compra_falha/",
            "pending": "http://127.0.0.1:8000/carrinho/compra_pendente/",
        },
        "auto_return": "all"
    }

    preference_response = sdk.preference().create(request)
    preference = preference_response["response"]

    return preference["init_point"]