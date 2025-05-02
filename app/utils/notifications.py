# Lógica de envío de notificaciones push vía OneSignal.
# Sustituye integración con Firebase.
# Creado por Ale el 02/05/2025

import requests
import os

# Cargar credenciales desde entorno (.env o config)
ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID")
ONESIGNAL_REST_API_KEY = os.getenv("ONESIGNAL_REST_API_KEY")

# Enviar notificación Push usando OneSignal
def enviar_notificacion_push(token_player_id: str, titulo: str, cuerpo: str) -> str:
    try:
        url = "https://onesignal.com/api/v1/notifications"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {ONESIGNAL_REST_API_KEY}"
        }

        payload = {
            "app_id": ONESIGNAL_APP_ID,
            "include_player_ids": [token_player_id],
            "headings": {"en": titulo},
            "contents": {"en": cuerpo}
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        return f"Notificación enviada: {response.json().get('id')}"
    except Exception as e:
        return f"Error al enviar notificación: {str(e)}"
