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
  git clone hhttps://github.com/AndwSX/Diven.git
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

#### 5. Instala las dependencias necesarias

```bash
  pip install fastapi uvicorn sqlalchemy pymysql jinja2 python-multipart pydantic[email]

```

#### 6. Inicia el servidor de desarrollo

```bash
  uvicorn main:app --reload
```

## Tecnologías

| Componente                      | Tecnología Usada                             | Descripción                                                                              |
|----------------------------------|----------------------------------------------|------------------------------------------------------------------------------------------|
| Backend (API y lógica de negocio)| 🐍 FastAPI                                   | Framework en Python para crear APIs rápidas y eficientes.                                |
| Base de datos                   | 🐬 MySQL        | Sistema de gestión de bases de datos relacional (SQL).                                   |
| ORM                             | 🔗 SQLAlchemy                                | Librería en Python para manejar bases de datos con objetos y consultas SQL.               |
| Autenticación                   | 🔒 JWT con `jose` y `passlib`                 | Manejo de sesiones seguras con tokens JWT.                                                |
| Frontend                        | 🌐 HTML, CSS, Bootstrap                      | Estructura y diseño visual de la aplicación.                                              |
| Interactividad en el Cliente    | ⚡ JavaScript (fetch API, eventos DOM)        | Conexión con la API, gestión del inventario en la interfaz.                               |
| Servidor web y ejecución        | 🚀 Uvicorn                                   | Servidor ASGI para ejecutar FastAPI.                                                      |

## 👥 Autores

- [@Joaquin-canon](https://github.com/Joaquin-canon)
- [@ZontPizzaLove1](https://github.com/ZontPizzaLove1)
- [@Zeus??¿](https://github.com/Diventracker)
- [@lolroll??¿](https://github.com/Diventracker)
- [@AndwSX](https://github.com/AndwSX)


---

¿Te gustaría contribuir?  
¡Siéntete libre de enviar un Pull Request o abrir un Issue!