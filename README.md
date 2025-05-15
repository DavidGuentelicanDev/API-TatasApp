<h1 align="center">📱 API TatasApp</h1>

### 👥 Creadores
- Alexander Aguilera  
- Andrea Pino  
- David Guentelican

---

## 🚀 Rutas Desplegadas

<details>
<summary><strong>👤 Usuarios</strong></summary>

- `POST` Registro de usuario  
- `GET` Contactos registrados (tipo 2 = familiar)  
- `GET` Obtener usuarios por ID  
- `GET` Obtener foto de perfil por ID  
- `POST` Login  
- `PATCH` Editar foto de perfil  
- `PATCH` Editar datos generales de usuario  
- `PATCH` Editar correo  
- `PATCH` Editar contraseña  

</details>

<details>
<summary><strong>👨‍👩‍👧 Familiares</strong></summary>

- `POST` Registro de familiar  
- `GET` Obtener familiares registrados en grupo familiar  
- `DELETE` Eliminar familiar del grupo familiar  

</details>

<details>
<summary><strong>📅 Eventos</strong></summary>

- `POST` Crear evento  
- `GET` Listar eventos  
- `DELETE` Eliminar evento  
- `PUT` Editar evento  
- `GET` Listar eventos por familiar  

</details>

<details>
<summary><strong>🚨 Alertas</strong></summary>

- `POST` Crear alerta  
- `GET` Obtener alertas pendientes por ID de familiar  
- `GET` Obtener alertas concretadas por ID de familiar  
- `PATCH` Actualizar estado de alertas  

</details>

---

## 🏗️ Arquitectura General

El proyecto está basado en una arquitectura de capas para APIs, que incluye:

- **Models**: Estructuras de datos con SQLAlchemy  
- **Schemas**: Validaciones y serializaciones con Pydantic  
- **Routers**: Controladores de rutas  
- **Utils**: Funciones auxiliares  
- **Settings**: Configuración centralizada  
- **Auth**: Lógica de autenticación (hashing y JWT)

---

## 🔧 Componentes Clave

### 🔸 Models
Definidos en `models.py` usando SQLAlchemy:
- `Usuario`, `Familiar`, `Evento`, `Alerta`

### 🔸 Schemas
En `schemas/` usando Pydantic:
- `UsuarioCreate`, `EventoOut`, etc.

### 🔸 Routers
En `routers/`:
- `usuario.py`, `alerta.py`, etc.

### 🔸 Settings
En `settings/`:
- Configuración de entorno y base de datos

### 🔸 Auth
En `auth/`:
- Hashing con `bcrypt`, JWT tokens

### 🔸 Utils
En `utils/`:
- Validaciones personalizadas y helpers

---

## 🔁 Flujo de Trabajo

1. 📥 Solicitud HTTP del cliente  
2. 🔀 Router correspondiente la procesa  
3. ✅ Validación con Pydantic  
4. 🧠 Lógica de negocio y consultas a la DB  
5. 📤 Respuesta serializada al cliente

---

## 🛠️ Características Adicionales

- 📦 **PostgreSQL** como base de datos  
- 🔐 **JWT** para autenticación  
- 🌐 **CORS** configurado  
- ⚠️ Manejo personalizado de errores y excepciones

---

## ✅ Ventajas de la Arquitectura

- 📦 Modularidad
- 🚀 Escalabilidad
- ♻️ Reutilización
- 🔐 Seguridad

---

> _Para más detalles técnicos, consulta los archivos fuente o contáctanos directamente._