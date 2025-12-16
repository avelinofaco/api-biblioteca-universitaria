import enum
from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime, Enum as SQLEnum, func
)
from sqlalchemy.orm import relationship
from . import Base

class ReservaStatus(enum.Enum):
    ativa = "ativa"         #aguardando disponibilidade
    atendida = "atendida"   #reserva foi convertida em empréstimo
    cancelada = "cancelada" #reserva foi cancelada pelo usuário ou sistema

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    livro_id = Column(Integer, ForeignKey("livros.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    posicao = Column(Integer, nullable=False, default=0)
    status = Column(SQLEnum(ReservaStatus), nullable=False, server_default=ReservaStatus.ativa.value)

    usuario = relationship("Usuario", back_populates="reservas")
    livro = relationship("Livro", back_populates="reservas")
