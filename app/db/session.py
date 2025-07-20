# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Conexión a la base de datos (aquí puede ser SQLite o cualquier otra base de datos que uses)
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/deos.db"  # Cambia esto según tu configuración

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
