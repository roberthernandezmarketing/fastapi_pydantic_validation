from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class Producto (BaseModel):
  nombre : str
  precio : float
  disponible : bool = True
  tags : List[str] = []
  descripcion : Optional[str] = None

@app.post("/productos/")
async def crear_producto(producto : Producto):
  return {"mensaje" : "Producto creado", "producto" : producto}