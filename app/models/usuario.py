import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, func, Index
from sqlalchemy.orm import relationship
from . import Base

class UsuarioRole(enum.Enum):
    aluno = "aluno"
    bibliotecario = "bibliotecario"
    admin = "admin"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    role = Column(SQLEnum(UsuarioRole), nullable=False, server_default=UsuarioRole.aluno.value)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    emprestimos = relationship("Emprestimo", back_populates="usuario", cascade="all, delete-orphan")
    reservas = relationship("Reserva", back_populates="usuario", cascade="all, delete-orphan")
    multas = relationship("Multa", back_populates="usuario", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_usuario_nome_email", "nome", "email"),)
