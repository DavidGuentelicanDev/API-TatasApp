# Contiene la lógica de login, verificación de credenciales y creación de tokens JWT.
# Creado por david el 15/04

from sqlalchemy.orm import Session
from app.models import Usuario
from app.auth.hashing import verificar_contrasena


#autentificacion de usuario
#creada por david el 20/04
def autentificar_usuario(db: Session, correo: str, contrasena: str) -> Usuario | None:
    #buscar usuario por correo
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()

    #si usuario no existe o no coincide con la contraseña: error
    if not usuario or not verificar_contrasena(contrasena, usuario.contrasena):
        return None

    #si todo esta bien, devuelve el usuario
    return usuario