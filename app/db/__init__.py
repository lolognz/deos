from app.db import models  # importa los modelos para que se registren
from app.db.session import engine, Base


def init_db():
    """Crear todas las tablas en la base si no existen."""
    Base.metadata.create_all(bind=engine)
