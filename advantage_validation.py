from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator
import re

app = FastAPI()

class Usuario(BaseModel):
  nombre : str = Field(..., min_length=3, max_length=50)
  email : EmailStr
  edad : int = Field(..., gt=0, lt=120)
  codigo_postal : str

  @field_validator('codigo_postal')
  def validar_codigo_postal(cls, v):
    if not re.match(r'^\d{5}$', v):
        raise ValueError('Código postal debe tener 5 digitos')
    return v
  
@app.post("/usarios/")
def crear_usuario(usuario: Usuario):
   return {
      "mensaje" : "Usuario creado exitosamente", 
      "datos"   : usuario
   }