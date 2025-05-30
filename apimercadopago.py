import mercadopago
from dotenv import load_dotenv
import os

def realizar_pagamento(items):
    load_dotenv()

    sdk = mercadopago.SDK(f'{os.getenv("MP_ACCESS_TOKEN")}')

    preference_data = {
        "items": items,
        "back_urls": {
            "success": "https://e98f-191-241-23-30.ngrok-free.app/carrinho/compra_realizada/",
            "failure": "https://e98f-191-241-23-30.ngrok-free.app/carrinho/compra_falha/",
            "pending": "https://e98f-191-241-23-30.ngrok-free.app/carrinho/compra_pendente/",
        },
        "auto_return": "all",
        "notification_url": "https://c782-2804-1254-2089-a700-e5dc-4b99-4201-1635.ngrok-free.app/webhook/mercadopago/",
        "external_reference": "pedido_1234",
    }

    preference_response = sdk.preference().create(preference_data)

    print("Resposta da API Mercado Pago:", preference_response)  # para debug

    # Verificar se a resposta tem o init_point
    if "response" in preference_response and "init_point" in preference_response["response"]:
        return preference_response["response"]["init_point"]
    else:
        # Logar erro ou lançar exceção amigável
        raise Exception(f"Erro ao criar link de pagamento: {preference_response}")
