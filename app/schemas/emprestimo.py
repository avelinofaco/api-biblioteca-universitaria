from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.multa import MultaOut
from typing import List


class EmprestimoCreate(BaseModel): # representa o que o cliente precisa enviar para criar um empréstimo
    usuario_id: int
    livro_id: int
    dias: Optional[int] = 14

class EmprestimoUpdate(BaseModel): # defina O que pode ser alterado depois que o empréstimo já existe
    # campos que podem ser atualizados manualmente (opcional)
    data_prevista_devolucao: Optional[datetime] = None
    data_devolucao: Optional[datetime] = None
    renovacoes: Optional[int] = None
    status: Optional[str] = None

class EmprestimoOut(BaseModel):  # define O que a API devolve para o cliente
    id: int
    usuario_id: int
    livro_id: int
    data_emprestimo: datetime
    data_prevista_devolucao: datetime
    data_devolucao: Optional[datetime] = None
    renovacoes: int
    status: str

# supondo que você já tem EmprestimoOut e MultaOut, só criamos o wrapper:
class EmprestimoDevolucaoOut(BaseModel): # Quando devolvo um livro, quero saber o empréstimo e, se existir, a multa gerada
    emprestimo: EmprestimoOut
    multa: Optional[MultaOut] = None


class PageEmprestimo(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[EmprestimoOut]


class RenovacaoEmprestimo(BaseModel):
    dias: int = Field(7, ge=1, le=30)

    class Config:      # "Esse schema pode ser criado a partir de objetos ORM (SQLAlchemy)"
        orm_mode = True
    
