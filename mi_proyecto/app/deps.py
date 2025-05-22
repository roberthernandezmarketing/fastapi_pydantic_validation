#
# deps.py : Dependencies
#
from database import SessionLocal, engine

# Dependencies to create a DB session - OJO: remove in main.py
# Función generadora que proporciona una sesión de base de datos.
# Depends es el mecanismo de FastAPI para implementar un patrón de diseño crucial que mejora 
# la modularidad, la mantenibilidad y la capacidad de prueba de tu código, al tiempo que 
# simplifica la gestión de recursos.

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()