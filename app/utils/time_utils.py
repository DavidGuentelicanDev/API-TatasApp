# Funciones relacionadas con manejo de fechas y horas: zonas horarias, cálculo de rangos, horarios nocturnos.
# Determinar si una hora está en rango nocturno (modo silencio)
# Calcular diferencias de tiempo para alertas de inactividad
# Parsear o formatear fechas y horas

# Creado por david el 15/04

from datetime import datetime
import pytz


ZH_CHILE = pytz.timezone('America/Santiago') #zona horaria de chile continental

#funcion para determinar la zona horaria de funcionamiento de la API
#creado por david el 29/04
def horario_actual():
    hora_actual = datetime.now(ZH_CHILE)
    return hora_actual.strftime('%Y-%m-%d %H:%M:%S')