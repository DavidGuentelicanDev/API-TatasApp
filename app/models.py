# Contiene los modelos ORM que definen las tablas de la base de datos.
# Creado por david el 15/04

from sqlalchemy import (
    Column,
    String,
    Text,
    BigInteger,
    Date,
    SmallInteger,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    DateTime,
    func
)
from sqlalchemy.orm import relationship
from app.database import Base


#tabla direccion
#creada por david el 15/04
class Direccion(Base):
    __tablename__ = "DIRECCION"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    direccion_texto = Column(Text, nullable=False)
    adicional = Column(String(100), nullable=True)

    #relacion inversa con usuario
    usuarios = relationship("Usuario", back_populates="direccion_rel")

#########################################################################################

#tabla usuario
#creada por david el 15/04
class Usuario(Base):
    __tablename__ = "USUARIO"

    #dict (diccionario) tipo_usuarios
    TIPOS_USUARIO = {
        1: "Adulto Mayor",
        2: "Familiar"
    }

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    direccion_id = Column(BigInteger, ForeignKey("DIRECCION.id"), nullable=False, index=True)
    correo = Column(String(100), nullable=False, unique=True, index=True)
    telefono = Column(String(9), nullable=False, unique=True, index=True)
    tipo_usuario = Column(SmallInteger, nullable=False, index=True)
    contrasena = Column(String(255), nullable=False)
    foto_perfil = Column(Text, nullable=True)
    token_fcm = Column(Text, nullable=True) #token para notificaciones push

    #relacion con tabla direccion
    direccion_rel = relationship("Direccion", back_populates="usuarios")
    #relaciones inversas con evento, rutina y alerta
    eventos = relationship("Evento", back_populates="usuarios")
    # rutinas = relationship("Rutina", back_populates="usuarios")
    alertas = relationship("Alerta", back_populates="usuarios")

    #definicion especial para tipo_usuario con check
    __table_args__ = (
        CheckConstraint("tipo_usuario BETWEEN 1 AND 2", name="check_tipo_usuario_valido"),
    )

    #propiedad que permite leer el tipo de usuario segun el valor int guardado
    @property
    def tipo_usuario_nombre(self):
        return self.TIPOS_USUARIO.get(self.tipo_usuario, "Desconocido")

#########################################################################################

#tabla familiar
#creada por Andrea el 25/04
class Familiar(Base):
    __tablename__ = "FAMILIAR"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    adulto_mayor_id = Column(BigInteger, ForeignKey("USUARIO.id"), nullable=False, index=True,)
    familiar_id = Column(BigInteger, ForeignKey("USUARIO.id"), nullable=False, index=True,)

    #relaciones
    adulto_mayor = relationship("Usuario", foreign_keys=[adulto_mayor_id], backref="familiares_asociados")
    familiar = relationship("Usuario", foreign_keys=[familiar_id], backref="adultos_mayores_asociados")

    #restricciones
    __table_args__ = (
        UniqueConstraint("adulto_mayor_id",  "familiar_id", name="uq_adulto_familiar"), #unique adulto_mayor_id y familiar_id combinados
        CheckConstraint('adulto_mayor_id <> familiar_id', name='check_ids_distintos') #check para no poder agregar el mismo id de usuario
    )

#########################################################################################

#tabla evento
#creada por david el 27/04
class Evento(Base):
    __tablename__ = "EVENTO"

    #diccionario de tipos de eventos
    TIPOS_EVENTO = {
        1: "Cita Médica",
        2: "Evento Familiar",
        3: "Evento Personal",
        4: "No se qué más puede ser"
    }

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(BigInteger, ForeignKey("USUARIO.id"), nullable=False, index=True)
    nombre = Column(String(30), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_hora = Column(DateTime, nullable=False, index=True)
    tipo_evento = Column(SmallInteger, nullable=False, index=True)

    #relacion con usuario
    usuarios = relationship("Usuario", back_populates="eventos")

    #check para tipo_evento: los limites de int que tendra
    __table_args__ = (
        CheckConstraint("tipo_evento BETWEEN 1 AND 4", name="check_tipo_evento_valido"),
    )

    #propiedad para leer el string de tipo_evento
    @property
    def tipo_evento_nombre(self):
        return self.TIPOS_EVENTO.get(self.tipo_evento, "Desconocido")

#########################################################################################

#tabla rutina
#creada por david el 27/04
# class Rutina(Base):
#     __tablename__ = "RUTINA"

#     #diccionario de tipos de rutina
#     TIPOS_RUTINA = {
#         1: "Medicamentos",
#         2: "Ejercicios",
#         3: "Etc..."
#     }

#     id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
#     usuario_id = Column(BigInteger, ForeignKey("USUARIO.id"), nullable=False, index=True)
#     nombre = Column(String(30), nullable=False)
#     descripcion = Column(Text, nullable=True)
#     tipo_rutina = Column(SmallInteger, nullable=False, index=True)

#     usuarios = relationship("Usuario", back_populates="rutinas") #relacion con usuario
#     dias_horas = relationship("DiaHora", back_populates="rutina") #relacion inversa con dia_hora

#     #check para tipo_rutina
#     __table_args__ = (
#         CheckConstraint("tipo_rutina BETWEEN 1 AND 3", name="check_tipo_rutina_valido"),
#     )

#     #propiedad para leer el string de tipo_evento
#     @property
#     def tipo_rutina_nombre(self):
#         return self.TIPOS_RUTINA.get(self.tipo_rutina, "Desconocido")

#########################################################################################

#tabla diahora (relacionada a rutina)
#creado por david rl 27/04
# class DiaHora(Base):
#     __tablename__ = "DIA_HORA"

#     id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
#     rutina_id = Column(BigInteger, ForeignKey("RUTINA.id"), nullable=False, index=True)
#     dia = Column(Date, nullable=False, index=True)
#     hora = Column(Time, nullable=False, index=True)

#     #relacion con rutina
#     rutina = relationship("Rutina", back_populates="dias_horas")

#     #restriccion para que no se repita la rutina el mismo dia a la misma hora
#     __table_args__ = (
#         UniqueConstraint("rutina_id", "dia", "hora", name="uq_rutina_dia_hora"),
#     )

#########################################################################################

#tabla alerta
#creado por david el 27/04
class Alerta(Base):
    __tablename__ = "ALERTA"

    #diccionario de tipos de eventos
    TIPOS_ALERTA = {
        1: "Zona Segura",
        2: "Inactividad",
        3: "Caída",
        4: "SOS"
    }

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(BigInteger, ForeignKey("USUARIO.id"), nullable=False, index=True)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    ubicacion = Column(Text, nullable=False) #se puede guardar como string
    mensaje = Column(Text, nullable=False)
    tipo_alerta = Column(SmallInteger, nullable=False, index=True)

    #relacion con usuario
    usuarios = relationship("Usuario", back_populates="alertas")

    #check para tipo_alerta
    __table_args__ = (
        CheckConstraint("tipo_alerta BETWEEN 1 AND 4", name="check_tipo_alerta_valido"),
    )

    #propiedad para leer el string de tipo_evento
    @property
    def tipo_alerta_nombre(self):
        return self.TIPOS_ALERTA.get(self.tipo_alerta, "Desconocido")
