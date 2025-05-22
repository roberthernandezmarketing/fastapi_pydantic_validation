#
# database.py : Setup DB connection
#
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexiön para SQLite (archivo local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Para PostgreSQL seria algo como:
# Ocultar en .env
# SQLALCHEMY_DATABASE_URL = "postgresql://usuario:contrasena@localhost/nombre_db"

# Crear el motor de SQLAlchemy
engine = create_engine(
  SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear sesion local para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase Base que sera la base para nuestros modelos
Base = declarative_base()

