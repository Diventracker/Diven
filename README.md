# 🚀 Diventracker Info

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- 🐍 [Python 3.10+](https://www.python.org/downloads/)
- 🐬 [MySQL Server](https://dev.mysql.com/downloads/mysql/)
- 📦 [pip](https://pip.pypa.io/en/stable/installation/) (gestor de paquetes de Python)
- 🌿 [Git](https://git-scm.com/) (para clonar el repositorio)

---

## 🛠️ Instrucciones de Instalación


#### 1. Clona el proyecto

```bash
  git clone https://github.com/Diventracker/Diven.git
```

#### 2. Entra en el directorio del proyecto

```bash
  cd Diven
```

#### 3. Crea un entorno virtual `venv`

```bash
  python -m venv venv
```

#### 4. Activa el entorno virtual


```bash

  venv\Scripts\activate (Windows)
  source venv/bin/activate (Linux/Mac)
```


#### 4.1 *Opcional - Si pide permisos (Ejecutar antes del activate)



```bash
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Unrestricted
```

#### 5. Instala las dependencias necesarias

```bash
  pip install -r requirements.txt
```

#### 6. Inicia el servidor de desarrollo

```bash
  uvicorn main:app --reload
```

## 👥 Usuarios de Ejemplo

| 📧 Correo                  | 🔒 Contraseña     |
|---------------------------|-------------------|
| admin@tienda.com      | clave123     |


---

## 🗂️ Estructura del Proyecto

```bash
/Diven/
├── 📄 main.py                # Punto de entrada de la app FastAPI
├── 📁 modulos/               # Módulos independientes organizados por funcionalidad
│   └── 🔁 routes.py             # Define las rutas (endpoints) y conecta con controllers
│   └── 🧠 controllers.py        # Lógica del negocio (servicios, reglas)
│   └── 🧱 models.py             # Modelos de SQLAlchemy (estructuras de la base de datos)
│   └── 🧾 schemas.py            # Schemas de Pydantic (validación y serialización de datos)
│   └── 🖥️templates/             # Archivos HTML usando Jinja2 para el renderizado
├── 🎨 static/                # Archivos estáticos (CSS, JS, imágenes, etc.)
├── 🧰 utils/                 # Funciones auxiliares o reutilizables
├── 🗃️ database/              # Configuración y conexión a la base de datos
└── 📋 requirements.txt       # Lista de dependencias del proyecto
```

## Tecnologías

| Componente                      | Tecnología Usada                             | Descripción                                                                              |
|----------------------------------|----------------------------------------------|------------------------------------------------------------------------------------------|
| Backend (API y lógica de negocio)| 🐍 FastAPI                                   | Framework en Python para crear APIs rápidas y eficientes.                                |
| Base de datos                   | 🐬 MySQL        | Sistema de gestión de bases de datos relacional (SQL).                                   |
| ORM                             | 🔗 SQLAlchemy                                | Librería en Python para manejar bases de datos con objetos y consultas SQL.               |
| Autenticación                   | 🔒 JWT con `passlib`                 | Manejo de sesiones seguras con tokens JWT.                                                |
| Frontend                        | 🌐 HTML, CSS, Bootstrap                      | Estructura y diseño visual de la aplicación.                                              |
| Interactividad en el Cliente    | ⚡ JavaScript (fetch API, eventos DOM)        | Conexión con la API, gestión del inventario en la interfaz.                               |
| Servidor web y ejecución        | 🚀 Uvicorn                                   | Servidor ASGI para ejecutar FastAPI.                                                      |

## 👥 Autores

- [@Joaquin-canon](https://github.com/Joaquin-canon)
- [@Deivit-Agudelo](https://github.com/ZontPizzaLove1)
- [@SergioMora-17](https://github.com/Diventracker)
- [@Harol_p??¿](https://github.com/Diventracker)
- [@AndwSX](https://github.com/AndwSX)


---

