import mercadopago
from dotenv import load_dotenv
import os

def realizar_pagamento(items):
    load_dotenv()

    sdk = mercadopago.SDK(f'{os.getenv("MP_ACCESS_TOKEN")}')

    preference_data = {
        "items": items,
        "back_urls": {
            "success": "http://127.0.0.1:8000/carrinho/compra_realizada/",
            "failure": "http://127.0.0.1:8000/carrinho/compra_falha/",
            "pending": "http://127.0.0.1:8000/carrinho/compra_pendente/",
        },
        "auto_return": "all",
        "notification_url": "https://c782-2804-1254-2089-a700-e5dc-4b99-4201-1635.ngrok-free.app/webhook/mercadopago/",
        "external_reference": "pedido_1234",
    }

    # Criar a preferência de pagamento
    preference_response = sdk.preference().create(preference_data)

    preference = preference_response["response"]
    return preference["init_point"]