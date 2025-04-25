# Diven
# Para Poder iniciar el proyecto hay que crear un entorno virtual e instalar las dependencias
# Con la carpeta del proyecto en visual, se colocan estos comandos en la consola...

python -m venv venv             //Entorno Virtual
venv\Scripts\activate        //Activar el entorno virtual

pip install fastapi uvicorn      //Instala fastapi y uvicorn
pip install sqlalchemy pymysql   // Para Usar base de datos MYSQl(xampp)
pip install jinja2               // PAra Cargar templates del html
pip install python-multipart     // para poder manejar el uso de formularios
pip install pydantic[email]     //Sirve para validar correos con pydantic

uvicorn main:app --reload     //Para ejecutar el archivo main en el puerto 8000
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Unrestricted   //Si pide permisos ejecutar este comando antes del uvicorn *Opcional
