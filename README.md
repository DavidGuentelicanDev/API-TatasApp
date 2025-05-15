--API TatasApp--

Creadores:
- Alexander Aguilera
- Andrea Pino
- David Guentelican

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

1. Arquitectura General
El proyecto utiliza una arquitectura de Capas adaptada para APIs, con una separación clara de responsabilidades:
- Modelos (Models): Define las estructuras de datos y las tablas de la base de datos utilizando SQLAlchemy.
- Esquemas (Schemas): Define las validaciones y serializaciones de datos con Pydantic.
- Rutas (Routers): Implementa los controladores de las rutas de la API.
- Utilidades (Utils): Contiene funciones auxiliares reutilizables, como validaciones y respuestas estándar.
- Configuración (Settings): Centraliza la configuración del proyecto, como variables de entorno y conexión a la base de datos.
- Autenticación (Auth): Maneja la lógica de autenticación, hashing de contraseñas y generación de tokens JWT.

2. Estructura de Carpetas
La estructura del proyecto está organizada de manera modular, lo que facilita la escalabilidad y el mantenimiento:

app/
├── main.py                # Punto de entrada de la aplicación FastAPI
├── models.py              # Modelos ORM para la base de datos
├── routers/               # Rutas de la API
│   ├── alerta.py
│   ├── evento.py
│   ├── familiar.py
│   ├── usuario.py
├── schemas/               # Esquemas de validación y serialización
│   ├── alerta.py
│   ├── evento.py
│   ├── familiar.py
│   ├── usuario.py
├── settings/              # Configuración y dependencias
│   ├── config.py          # Variables de entorno y configuración
│   ├── database.py        # Configuración de la base de datos
│   ├── dependencies.py    # Dependencias reutilizables (e.g., sesiones de DB)
├── auth/                  # Lógica de autenticación
│   ├── auth.py            # Verificación de credenciales
│   ├── hashing.py         # Hashing de contraseñas
│   ├── jwt.py             # Generación y validación de tokens JWT
├── utils/                 # Funciones auxiliares
│   ├── helpers.py         # Validaciones y utilidades generales
│   ├── validations.py     # Manejo de excepciones personalizadas

3. Componentes Clave
a. Modelos (Models)
Definidos en models.py, representan las tablas de la base de datos con SQLAlchemy. Ejemplo:
- Usuario: Representa a los usuarios del sistema.
- Familiar: Relaciona a los usuarios con sus familiares.
- Evento y Alerta: Representan eventos y alertas asociados a los usuarios.

b. Esquemas (Schemas)
Definidos en schemas, utilizan Pydantic para validar y serializar datos de entrada/salida. Ejemplo:
- UsuarioCreate: Valida los datos para registrar un usuario.
- EventoOut: Serializa los datos de un evento para la respuesta.

c. Rutas (Routers)
Definidas en routers, agrupan las rutas de la API por funcionalidad. Ejemplo:
- usuario.py: Maneja el registro, login y actualización de usuarios.
- alerta.py: Maneja la creación y consulta de alertas.

d. Configuración (Settings)
Centralizada en settings, incluye:
- Variables de entorno cargadas desde .env (e.g., claves secretas, configuración de la base de datos).
- Configuración de la base de datos con SQLAlchemy.

e. Autenticación (Auth)
Definida en auth, incluye:
- Hashing de contraseñas con bcrypt.
- Generación y validación de tokens JWT.

f. Utilidades (Utils)
Definidas en utils, incluyen:
- Validaciones personalizadas (e.g., fechas futuras, correos válidos).
- Respuestas JSON estándar.

4. Flujo de Trabajo
- Solicitud HTTP: El cliente realiza una solicitud a una ruta específica.
- Router: La solicitud es manejada por un router en routers.
- Validación: Los datos de entrada son validados por un esquema en schemas.
- Lógica de Negocio: Se ejecuta la lógica de negocio, interactuando con los modelos en models.py.
- Respuesta: Los datos son serializados y devueltos al cliente.

5. Características Adicionales
- Base de Datos: Utiliza PostgreSQL como base de datos relacional.
- Autenticación: Implementa autenticación basada en JWT.
- CORS: Configurado para permitir solicitudes desde orígenes específicos.
- Manejo de Errores: Handlers personalizados para errores de validación y excepciones HTTP.

6. Ventajas de la Arquitectura
- Modularidad: Cada funcionalidad está separada en módulos, facilitando el mantenimiento.
- Escalabilidad: La estructura permite agregar nuevas funcionalidades sin afectar las existentes.
- Reutilización: Las dependencias y utilidades son reutilizables en diferentes partes del proyecto.
- Seguridad: Uso de hashing seguro para contraseñas y autenticación con JWT.