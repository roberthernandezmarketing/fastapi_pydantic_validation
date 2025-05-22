#
# crud.py : CRUD DB operations 23:22
#
from sqlalchemy.orm import Session
import models, schemas

# Session: En SQLAlchemy, una Session es tu interfaz principal para la base de datos. 
# Es como una "conversación" con la base de datos. 
# A través de la sesión, puedes realizar consultas, añadir nuevos objetos, modificar existentes, 
# y luego "commit" (confirmar) esos cambios a la base de datos de forma transaccional. 
# Es fundamental para interactuar con la base de datos usando SQLAlchemy.


# READ / GET / SQL SELECT
def get_user(db: Session, user_id: int) :
  return db.query(models.User).filter(models.User.id == user_id).first()
#  Inicia una consulta a la base de datos a través de la sesión db. 
#  Le estás diciendo a SQLAlchemy que quieres consultar la tabla de User 
#  (representada por models.User, tu modelo ORM para la tabla de usuarios).

# READ / GET / SQL SELECT
def get_user_by_email(db: Session, email: str) :
  return db.query(models.User).filter(models.User.email == email) .first()

# READ / GET / SQL SELECT
def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.User).offset(skip).limit(limit).all()


# CREATE / POST / SQL INSERT
def create_user(db: Session, user: schemas.UserCreate) :
  
  # En un entorno real, usarías una librería de hashing segura como bcrypt o Argon2 antes de almacenar el password
  fake_hashed_password = user. password + "notreallyhashed"

  db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

# READ / GET / SQL SELECT
def get_items(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Item).offset(skip).limit(limit).all()

# CREATE / POST / SQL INSERT
def create_user_item(db: Session, item: schemas.ItemCreate, user_id:int):
    # Crea una instancia del modelo ORM de SQLAlchemy para el Item.
    # 'item.dict()' convierte el esquema Pydantic (schemas.ItemCreate)
    # en un diccionario de atributos. El '**' desempaqueta este diccionario
    # para pasarlos como argumentos de palabra clave al constructor de models.Item.
    # El 'owner_id' se añade explícitamente ya que no está en schemas.ItemCreate,
    # pero es necesario para la relación en models.Item.
  db_item = models.Item(**item.dict(), owner_id=user_id)

  db.add (db_item)
  db.commit()
  db.refresh(db_item)
  return db_item

# UPDATE / PUT / SQL UPDATE
def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
  db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
  if db_item is None:
    return None
  
  # Actualizar los atributos del item
  for key, value in item.dict().items():
    # Usa 'setattr' para establecer el valor del atributo 'key'
    # en el objeto ORM 'db_item' con el 'value' correspondiente.
    # Por ejemplo, si 'key' es "title" y 'value' es "New Title",
    # esto es equivalente a 'db_item.title = "New Title"'.
    setattr(db_item, key, value)

  db.commit()
  db.refresh(db_item)
  return db_item

# UPDATE / PUT / SQL DELETE
def delete_item(db: Session, item_id: int):
  db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
  if db_item is None:
    return False
  db.delete(db_item)
  db.commit()
  return True
