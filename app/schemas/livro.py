from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LivroBase(BaseModel):
    titulo: str
    autor: Optional[str] = None
    isbn: Optional[str] = None
    quantidade_total: int = 1
    area: Optional[str] = None

class LivroCreate(LivroBase):
    pass

class LivroUpdate(BaseModel):
    titulo: Optional[str]
    autor: Optional[str]
    isbn: Optional[str]
    quantidade_total: Optional[int]
    area: Optional[str]

class LivroOut(LivroBase):
    id: int
    quantidade_disponivel: int
    created_at: datetime

    class Config:
        orm_mode = True
