import enum
from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime, Enum as SQLEnum, Numeric, Text, func
)
from sqlalchemy.orm import relationship
from . import Base

class MultaStatus(enum.Enum):
    pendente = "pendente"
    paga = "paga"
    cancelada = "cancelada"

class Multa(Base):
    __tablename__ = "multas"

    id = Column(Integer, primary_key=True)
    emprestimo_id = Column(Integer, ForeignKey("emprestimos.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    descricao = Column(Text, nullable=True)
    status = Column(SQLEnum(MultaStatus), nullable=False, server_default=MultaStatus.pendente.value)
    gerada_em = Column(DateTime, server_default=func.now(), nullable=False)
    paga_em = Column(DateTime, nullable=True)

    emprestimo = relationship("Emprestimo", back_populates="multas")
    usuario = relationship("Usuario", back_populates="multas")
