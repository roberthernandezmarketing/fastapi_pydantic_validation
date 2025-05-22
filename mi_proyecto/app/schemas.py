#
# schemas.py : Pydantic models to data validation 18:06
#
# Contiene los modelos Pydantic que usamos para la validación y serialización de datos de 
# entrada/salida de la API.
#
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# BaseModel: Esta es la clase más importante de Pydantic. 
# Todas tus clases de modelos de datos Pydantic deben heredar de BaseModel. 
# Proporciona la funcionalidad central para la validación, la serialización, 
#   la generación de esquemas JSON, etc.


# Modelo base para un Item. Define los atributos comunes a todas las representaciones
#   de un Item, como su título y una descripción opcional.
class ItemBase(BaseModel) :
  title      : str
  description: Optional[str] = None


# Modelo para la creación de un Item. Hereda de ItemBase, lo que significa
#   que tendrá 'title' y 'description'. No añade campos adicionales,
#   indicando que para crear un Item solo se necesitan los campos base.
#   Aunque tiene un PASS, se crea para darle mas claridad al codigo al tener 
#   por separado la creacion de un Item (ItemCreate) y la consulta del item (ItemBase)
class ItemCreate(ItemBase) :
  pass

# Modelo para la representación completa de un Item (tal como se leería de la DB).
#   Hereda de ItemBase y añade campos como 'id' y 'owner_id' que serían asignados
#   por la base de datos.
class Item(ItemBase) :
  id      : int
  owner_id: int

# class Config es una Clase de configuración interna para Pydantic.
# 
# orm_mode = True # Configura el modelo para ser compatible con ORMs (Object-Relational Mappers).
#                 # Esto permite que el modelo pueda leer datos directamente de una
#                 # instancia de objeto ORM (como un objeto SQLAlchemy),
#                 # convirtiendo automáticamente los atributos del objeto ORM
#                 # a los campos del modelo Pydantic.
#                 # Por ejemplo, si tienes un objeto 'item_db.title' y 'item_db.id',
#                 # Pydantic puede mapearlos directamente a 'Item.title' y 'Item.id'.
  class Config:
    orm_mode = True

# Modelo base para un Usuario. Define el atributo básico que identifica a un usuario.
class UserBase(BaseModel) :
  email: EmailStr

# Modelo para la creación de un Usuario. Hereda de UserBase y añade
#   el campo 'password', que es necesario al registrar un nuevo usuario
#   pero no debería ser devuelto en las respuestas de la API por seguridad.
class UserCreate(UserBase):
  password: str

# Modelo para la representación completa de un Usuario (tal como se leería de la DB).
#   Hereda de UserBase y añade campos adicionales asignados por la DB
#   o relacionados con su estado.
class User(UserBase):
  id        : int
  is_active : bool
  created_at: datetime
  items     : List[Item] = []
#             Una lista de Items que pertenecen a este usuario.
#             El valor por defecto es una lista vacía.
#             Pydantic validará que cada elemento de la lista
#             sea un objeto que se ajuste al esquema 'Item'.

# Clase de configuración interna para Pydantic.
  class Config:
    orm_mode = True
#   Habilita la compatibilidad con ORMs, permitiendo que
#   los objetos de usuario de la base de datos se conviertan
#   fácilmente a este esquema Pydantic.
#   Esto es crucial para la relación 'items': Pydantic
#   intentará cargar los objetos 'Item' relacionados.
