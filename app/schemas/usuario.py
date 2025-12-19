from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import List

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

class PageUsuario(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[UsuarioOut]
    class Config:
        orm_mode = True
