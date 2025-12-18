from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    password: str

class UsuarioCreate(UsuarioBase):
    role: Optional[str] = "aluno"

class UsuarioUpdate(BaseModel):
    nome: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]

class UsuarioOut(UsuarioBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        orm_mode = True
