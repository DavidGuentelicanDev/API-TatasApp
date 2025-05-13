--API TatasApp--

RUTAS DESPLEGADAS:

Usuarios:

- Registro de usuario (POST)
- Contactos registrados (tipo 2 = familiar) (GET)
- Obtener usuarios por id (GET)
- Obtener foto de perfil por id (GET)
- Login (POST)
- Editar foto de perfil (PATCH)
- Editar datos generales de usuario (PATCH)
- Editar correo (PATCH)
- Editar contraseña (PATCH)

Familiares:

- Registro de familiar (POST)
- Obtener familiares registrados en grupo familiar (adulto mayor) (GET)
- Eliminar familiar del grupo familiar (DELETE)

Eventos:

- Crear evento (POST)
- Listar eventos (GET)
- Eliminar evento (DELETE)
- Editar evento (PUT)
- Listar eventos por familiar (GET)

Alertas:

- Crear alerta (POST)
- Obtener alertas pendientes por id de familiar (GET)
- Obtener alertas concretadas por id de familiar (GET)
- Actualizar estado de alertas (para notificaciones) (PATCH)