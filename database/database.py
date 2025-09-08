import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Intenta leer la variable de entorno (Railway la define como DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Si no existe, asumimos que estás en local
    DATABASE_URL = "mysql+pymysql://root:@localhost/tienda_tecnologia"

# Crea la conexión
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base para modelos
Base = declarative_base()
