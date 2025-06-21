from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URI de conexión; en dev usaremos SQLite local
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/deos.db"

# engine: conecta con la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # sólo para SQLite
)

# session local: cada petición la puede obtener con SessionLocal()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()
