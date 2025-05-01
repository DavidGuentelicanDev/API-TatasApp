# Lógica de envío o simulación de notificaciones (voz, texto, push).
# Envío de mensajes de alerta (por ahora locales, en el futuro push/SMS)
# Simulación de lectura de voz para el adulto mayor

# Creado por david el 15/04

import firebase_admin
from firebase_admin import credentials
import json
from app.config import settings


#inicializar firebase admin sdk
#creado por david el 29/04
def inicializar_firebase():
    try:
        if not firebase_admin._apps:
            cred_dict = json.loads(settings.GOOGLE_APPLICATION_CREDENTIALS_JSON)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK inicializado correctamente")
        return "Firebase Admin SDK inicializado correctamente"
    except Exception as e:
        print(f"Error al inicializar Firebase Admin SDK: {str(e)}")
        return f"Error al inicializar Firebase Admin SDK: {str(e)}"
