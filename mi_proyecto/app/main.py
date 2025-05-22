# 
# Main.py : Access point to API    30:15
#
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

# Depends: Una función de FastAPI que se utiliza para la inyección de dependencias. 
# Es un patrón poderoso que permite a FastAPI manejar la creación y cierre de recursos 
# (como las sesiones de base de datos) y pasar estos recursos a tus funciones de path operation.


# Create tables in DB
# contiene todas las definiciones de tablas que has creado.
models.Base.metadata.create_all(bind=engine)
# create_all(bind=engine): Le dice a SQLAlchemy que "cree todas las tablas" definidas 
# en models.Base.metadata en la base de datos a la que está conectado el engine.
# Propósito: Esta línea se ejecuta al iniciar la aplicación para asegurar que todas las 
# tablas necesarias existen en la base de datos. Si las tablas ya existen, SQLAlchemy no las recreará.

app = FastAPI()

# Dependencies to create a DB session - OJO: move to deps.py
# Función generadora que proporciona una sesión de base de datos.
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# Endpoints - OJO: move to routes.py
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = crud.get_user_by_email(db, email=user.email)
  if db_user:
    raise HTTPException(status_code=400, detail="Email already registered")
  return crud.create_user(db=db, user=user)

#
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  users = crud.get_users(db, skip=skip, limit=limit)
  return users

#
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
  db_user = crud.get_user(db, user_id=user_id)
  if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  return db_user

#
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
  db_user = crud.get_user(db, user_id=user_id)
  if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  return crud.create_user_item(db=db, item=item, user_id=user_id)

#
@app.get( "/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends (get_db)):
  items = crud.get_items(db, skip=skip, limit=limit)
  return items

#
@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
  db_item = crud.update_item(db, item_id=item_id, item=item)
  if db_item is None:
    raise HTTPException(status_code=404, detail="Item not found")
  return db_item

#
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
  success = crud.delete_item(db, item_id=item_id)
  if not success:
    raise HTTPException(status_code=404, detail="Item not found")
  return {"detail": "Item deleted successfully"}



