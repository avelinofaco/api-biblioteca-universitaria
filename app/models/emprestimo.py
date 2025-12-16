import enum
from sqlalchemy import (
    Column,   # define colunas da tabela
    Integer,  # define tipo inteiro
    ForeignKey, # define chave estrangeira
    DateTime,   # define tipo data e hora
    Enum as SQLEnum, # enumeração no banco (SQL)
    func,            # funções SQL, como func.now()
    UniqueConstraint # regra de unicidade entre várias colunas
)
from sqlalchemy.orm import relationship #relacionamentos entre tabelas
from . import Base    #transforma a classe em tabela do banco

class EmprestimoStatus(str, enum.Enum): #cria enum e faz ele se comportar como string
    ativo = "ativo"
    devolvido = "devolvido"
    atrasado = "atrasado"

class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id = Column(Integer, primary_key=True)   #chave primária
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False) #chave estrangeira para tabela usuarios
    livro_id = Column(Integer, ForeignKey("livros.id", ondelete="CASCADE"), nullable=False)     #chave estrangeira para tabela livros
    data_emprestimo = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)             #data e hora do empréstimo
    data_prevista_devolucao = Column(DateTime(timezone=True), nullable=False)         #Até quando o usuário deve devolver o livro
    data_devolucao = Column(DateTime(timezone=True), nullable=True)                  #data e hora da devolução do livro
    renovacoes = Column(Integer, nullable=False, default=0)          #número de renovações do empréstimo
    status = Column(SQLEnum(EmprestimoStatus), nullable=False, server_default=EmprestimoStatus.ativo.value)  #status do empréstimo ativo por padrão

    usuario = relationship("Usuario", back_populates="emprestimos")   #relacionamento com a tabela usuarios
    livro = relationship("Livro", back_populates="emprestimos")       #relacionamento com a tabela livros
    multas = relationship("Multa", back_populates="emprestimo", cascade="all, delete-orphan")  #relacionamento com a tabela multas 

    __table_args__ = (
        # Atenção: essa constraint foi pensada para impedir duplicidade de empréstimo "ativo"
        # entre o mesmo usuário e livro. Pode precisar de checagem adicional na camada app
        # dependendo do DB/ORM e da forma de atualização do campo status.
        UniqueConstraint("usuario_id", "livro_id", "status", name="uq_usuario_livro_status"), #“Não pode existir mais de um empréstimo com o mesmo usuário, o mesmo livro e o mesmo status”.
    )
