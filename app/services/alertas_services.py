# Lógica de negocio relacionada a las alertas SOS, caídas, inactividad y zona segura.
# Servicios relacionados con alertas de caída, el botón SOS, la notificación a los familiares
# y otros eventos de alerta.
# Métodos para activar y notificar alertas (por ejemplo, el servicio que envía la ubicación
# del adulto mayor a los familiares).
# Integración con sensores o ubicación del dispositivo.
# Creado por david el 15/04


# servicio para crear una nueva alerta
# creado por Ale el 02/05/2025
from sqlalchemy.orm import Session
from app.models import Alerta
from app.schemas import AlertaCreate

def crear_alerta(alerta_data: AlertaCreate, db: Session) -> Alerta:
    nueva_alerta = Alerta(
        usuario_id=alerta_data.usuario_id,
        ubicacion=alerta_data.ubicacion,
        mensaje=alerta_data.mensaje,
        tipo_alerta=alerta_data.tipo_alerta
    )
    db.add(nueva_alerta)
    db.commit()
    db.refresh(nueva_alerta)
    return nueva_alerta