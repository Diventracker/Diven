from sqlalchemy import create_engine #Funcion que usa alchemy para conectarse a la bd
from sqlalchemy.orm import sessionmaker, declarative_base #mas funciones que es mejor preguntar xd

# Valores para conectar la base de datos con MYSQL(xampp)
DATABASE_URL = "mysql+pymysql://root:@localhost/tienda_tecnologia"

engine = create_engine(DATABASE_URL) #Crea la conexion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Función para obtener una sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base() #base para los modelos
