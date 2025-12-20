
#“Tradutor entre o mundo do negócio e o mundo da aplicação”.
from sqlalchemy.orm import Session
from app.crud import emprestimo as emprestimo_crud
from app.domain.exceptions import DomainError
from app.services.exceptions import BusinessRuleError, NotFoundError
from app import models, schemas
from app.services import historico_service
from datetime import datetime, timezone
from decimal import Decimal

# Serviço para criar um empréstimo
def criar_emprestimo_sevice(db: Session, payload: schemas.EmprestimoCreate):
    try:
        return emprestimo_crud.create(db, payload)

    except DomainError as e:
        raise BusinessRuleError(str(e))


VALOR_MULTA_POR_DIA = Decimal("2.00")
def devolver_emprestimo_service(db: Session, emprestimo_id: int):
    emprestimo = emprestimo_crud.get_by_id(db, emprestimo_id)

    if not emprestimo:
        raise NotFoundError("Empréstimo não encontrado.")

    if emprestimo.status != models.EmprestimoStatus.ativo:
        raise BusinessRuleError("Empréstimo não está ativo.")

    agora = datetime.now(timezone.utc)

    dias_atraso = 0
    valor_multa = Decimal("0.00")
    multa_obj = None

    if agora > emprestimo.data_prevista_devolucao:
        dias_atraso = max(
            (agora.date() - emprestimo.data_prevista_devolucao.date()).days,
            1
        )
        valor_multa = (Decimal(dias_atraso) * VALOR_MULTA_POR_DIA).quantize(
            Decimal("0.01")
        )

        multa_obj = models.Multa(
            emprestimo_id=emprestimo.id,
            usuario_id=emprestimo.usuario_id,
            valor=valor_multa,
            descricao=f"Multa por {dias_atraso} dia(s) de atraso",
            status=models.MultaStatus.pendente
        )
        db.add(multa_obj)

    # devolução física (persistência)
    emprestimo = emprestimo_crud.devolver_emprestimo(db, emprestimo, devolvido_em=agora)

    # 🔥 histórico consistente(sempre)
    historico_service.registrar_historico_devolucao(
        db=db,
        usuario_id=emprestimo.usuario_id,
        emprestimo_id=emprestimo.id,
        devolvido_em=agora,
        dias_atraso=dias_atraso,
        multa_gerada=valor_multa
    )
    db.commit()
    db.refresh(emprestimo)
    if multa_obj:
        db.refresh(multa_obj)


    return {
        "emprestimo": emprestimo,
        "multa": multa_obj
    }

def renovar_emprestimo_service(db: Session, emprestimo_id: int, payload: schemas.RenovacaoEmprestimo):
    emp = emprestimo_crud.renovar_emprestimo(db=db, emprestimo_id=emprestimo_id, dias=payload.dias)
    if not emp:
        raise BusinessRuleError(
            "Empréstimo não encontrado ou não está ativo."
        )
    return emp


def listar_emprestimos_service(db: Session,skip: int,limit: int):
    items = emprestimo_crud.get_all(db, skip, limit)
    total = emprestimo_crud.count(db)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }

def listar_ativos_service(db: Session, skip: int, limit: int):
    total = emprestimo_crud.count_ativos(db)
    items = emprestimo_crud.get_ativos(db, skip, limit)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }

 
def deletar_emprestimo_service(db: Session, emprestimo_id: int):
    res = emprestimo_crud.delete(db, emprestimo_id)

    if not res:
        raise NotFoundError("Empréstimo não encontrado.")

    return None
