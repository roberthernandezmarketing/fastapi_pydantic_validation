#
# crud.py : CRUD DB operations 23:22
#
from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException

# READ / GET
def get_user(db: Session, user_id: int) :
  return db. query(models.User).filter(models.User.id == user_id).first()

# READ / GET
def get_user_by_email(db: Session, email: str) :
  return db.query(models.User).filter(models.User.email == email) .first()

# READ / GET
def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.User).offset(skip).limit(limit).all()

# CREATE / POST
def create_user(db: Session, user: schemas.UserCreate) :
  
  fake_hashed_password = user. password + "notreallyhashed"

  db_user = models.User(email=user.email, hashed_password = fake_hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

#
def get_items(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Item).offset(skip).limit(limit).all()

#
def create_user_item(db: Session, item: schemas.ItemCreate, user_id:int):
  db_item = models.Item(**item.dict(), owner_id=user_id)
  db.add (db_item)
  db.commit()
  db.refresh(db_item)
  return db_item

#
def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
  db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
  if db_item is None:
    return None
  
  # Actualizar los atributos del item
  for key, value in item.dict().items():
    setattr(db_item, key, value)
  db.commit()
  db.refresh(db_item)
  return db_item

#
def delete_item(db: Session, item_id: int):
  db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
  if db_item is None:
    return False
  db.delete(db_item)
  db.commit()
  return True
