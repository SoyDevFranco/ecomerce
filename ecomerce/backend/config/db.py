from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus

# Codifica la contraseña para evitar problemas con caracteres especiales
password = quote_plus("Francoduarte2024")

# URL de conexión a la base de datos
DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/ecomercedb"

# Creación del motor SQLAlchemy
engine = create_engine(DATABASE_URL)

# Creación de la sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaración de una clase Base para ser utilizada como clase base para modelos declarativos
Base = declarative_base()


def get_db():
    """Crea una sesión de base de datos local y la cierra al finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
