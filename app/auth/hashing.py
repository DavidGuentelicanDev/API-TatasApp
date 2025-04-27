# Proporciona funciones para hashear y verificar contraseñas con bcrypt.
# Creado por david el 15/04

from passlib.context import CryptContext


#creado por david el 17/04
#configuracion del contexto del hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#se genera un hash seguro usando bcrypt
def get_hash_contrasena(contrasena: str) -> str:
    return pwd_context.hash(contrasena)

#verifica si una contraseña en texto plano coincide con el hash almacenado
def verificar_contrasena(contrasena_plana: str, contrasena_hasheada: str) -> bool:
    return pwd_context.verify(contrasena_plana, contrasena_hasheada)
