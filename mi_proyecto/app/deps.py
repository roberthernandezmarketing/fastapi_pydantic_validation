#
# deps.py : Dependencies
#
from database import SessionLocal, engine

# Dependencies to create a DB session - OJO: move to deps.py
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()