from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class Usuario(BaseModel):
  nombre : str = Field(..., min_length=3, max_length=50)
  email = 