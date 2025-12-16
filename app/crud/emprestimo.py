from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone #datetime representa data e hora, timedelta representa diferença entre datas/horas, timezone para fuso horário
from decimal import Decimal #Decimal para valores monetários com precisão
from app import models, schemas # models: modelos do banco de dados, schemas: esquemas Pydantic para entrada/saída de dados
from app.domain.exceptions import UsuarioNaoEncontrado, UsuarioComMultaPendente, LimiteEmprestimosExcedido, EmprestimoInvalido

# Função para criar um novo empréstimo

MAX_EMPRESTIMOS_ATIVOS = 2  # Limite máximo de empréstimos ativos por usuário
DIAS_PADRAO_EMPRESTIMO = 14  # Número padrão de dias para devolução do livro
def create(db: Session, emprestimo: schemas.EmprestimoCreate):
    # 1️. Usuário precisa existir
    if not usuario_existe(db, emprestimo.usuario_id):
        raise UsuarioNaoEncontrado("Usuário não cadastrado.")

    # 2️. Usuário não pode ter multas pendentes
    if usuario_tem_multas_pendentes(db, emprestimo.usuario_id):
        raise UsuarioComMultaPendente("Usuário possui multas pendentes.")

    # 3️. Usuário não pode ultrapassar limite de empréstimos ativos
    ativos = quantidade_emprestimos_ativos(db, emprestimo.usuario_id)
    if ativos >= MAX_EMPRESTIMOS_ATIVOS:
        raise LimiteEmprestimosExcedido("Limite de empréstimos ativos atingido.")

    # 4. datas sempre em UTC (timezone.utc) 
    agora = datetime.now(timezone.utc)
    dias = emprestimo.dias or DIAS_PADRAO_EMPRESTIMO
    data_prevista = agora + timedelta(days=dias)

    # 5. Criar o empréstimo
    db_emp = models.Emprestimo(
        usuario_id=emprestimo.usuario_id,
        livro_id=emprestimo.livro_id,
        data_emprestimo=agora,
        data_prevista_devolucao=data_prevista,
        status=models.EmprestimoStatus.ativo,
        renovacoes=0
    )
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

# Função para obter todos os empréstimos com paginação
def get_all(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Emprestimo)
        .offset(skip)
        .limit(limit)
        .all()
    )

# Função para obter um empréstimo por ID
def get_by_id(db: Session, emprestimo_id: int):
    return db.query(models.Emprestimo).filter(models.Emprestimo.id == emprestimo_id).first()

# Função para atualizar um empréstimo
def update(db: Session, emprestimo_id: int, emprestimo: schemas.EmprestimoUpdate):
    db_emp = get_by_id(db, emprestimo_id)
    if not db_emp:
        return None
    for key, value in emprestimo.model_dump(exclude_unset=True).items():
        setattr(db_emp, key, value)
    db.commit()
    db.refresh(db_emp)
    return db_emp


def delete(db: Session, emprestimo_id: int):
    db_emp = get_by_id(db, emprestimo_id)
    if not db_emp:
        return None
    db.delete(db_emp)
    db.commit()
    return {"message": "Empréstimo deletado com sucesso"}


VALOR_MULTA_POR_DIA = Decimal("2.00")

def devolver_emprestimo(db: Session, emprestimo_id: int):
    emprestimo = get_by_id(db, emprestimo_id)
    if not emprestimo:
        return None

    if emprestimo.status != models.EmprestimoStatus.ativo:
        return None

    agora = datetime.now(timezone.utc)

    emprestimo.data_devolucao = agora
    emprestimo.status = models.EmprestimoStatus.devolvido

    multa_obj = None
    if agora > emprestimo.data_prevista_devolucao:
        dias_atraso = max(
            (agora.date() - emprestimo.data_prevista_devolucao.date()).days,
            1
        )

        valor = (Decimal(dias_atraso) * VALOR_MULTA_POR_DIA).quantize(
            Decimal("0.01")
        )

        multa_obj = models.Multa(
            emprestimo_id=emprestimo.id,
            usuario_id=emprestimo.usuario_id,
            valor=valor,
            descricao=f"Multa por {dias_atraso} dia(s) de atraso",
            status=models.MultaStatus.pendente
        )

        db.add(multa_obj)

    db.commit()

    db.refresh(emprestimo)
    if multa_obj:
        db.refresh(multa_obj)

    return {
        "emprestimo": emprestimo,
        "multa": multa_obj
    }


def renovar_emprestimo(db: Session, emprestimo_id: int, dias: int = 7):
    emprestimo = get_by_id(db, emprestimo_id)
    if not emprestimo:
        return None

    if emprestimo.status != models.EmprestimoStatus.ativo:
        return None
    
    emprestimo.data_prevista_devolucao += timedelta(days=dias)
    emprestimo.renovacoes += 1
    db.commit()
    db.refresh(emprestimo)
    return emprestimo

# Função para obter todos os empréstimos ativos
def get_ativos(db: Session):
    return (
        db.query(models.Emprestimo)
        .filter(models.Emprestimo.status == models.EmprestimoStatus.ativo)
        .all()
    )


# Função para obter todos os empréstimos ativos por usuário
def get_ativos_por_usuario(db: Session, usuario_id: int):
    return (
        db.query(models.Emprestimo)
        .filter(
            models.Emprestimo.usuario_id == usuario_id,
            models.Emprestimo.status == models.EmprestimoStatus.ativo
        )
        .all()
    )


# Função para verificar se o usuário existe
def usuario_existe(db: Session, usuario_id: int) -> bool:
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first() is not None


# Função para verificar se o usuário tem multas pendentes
def usuario_tem_multas_pendentes(db: Session, usuario_id: int) -> bool:
    return (
        db.query(models.Multa)
        .filter(
            models.Multa.usuario_id == usuario_id,
            models.Multa.status == models.MultaStatus.pendente
        )
        .first()
        is not None
    )

# Função para contar a quantidade de empréstimos ativos de um usuário
def quantidade_emprestimos_ativos(db: Session, usuario_id: int) -> int:
    return (
        db.query(models.Emprestimo)
        .filter(
            models.Emprestimo.usuario_id == usuario_id,
            models.Emprestimo.status == models.EmprestimoStatus.ativo
        )
        .count()
    )
