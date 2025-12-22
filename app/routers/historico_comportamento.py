from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.services import historico_service

from app import schemas, models
from app.deps import get_db, get_current_user
from app.services import historico_service
from app.dependencies.permissions import exigir_roles

router = APIRouter(prefix="/historico", tags=["historico"])


# Usuario logado pode ver seu historico de devoluçoes
@router.get("/me",response_model=schemas.PageHistoricoOut,
        summary="Listar meu histórico de comportamento",
        description="cada usuario ver seu historico de comportamento(com base nas devoluções)")
def meu_historico(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100),
        db: Session = Depends(get_db),
        usuario_logado: models.Usuario = Depends(get_current_user)):
    return historico_service.listar_historico_usuario_service(
        db=db,
        usuario_id=usuario_logado.id,
        skip=skip,
        limit=limit
    )


# Listar histórico de um usuário quaquer
@router.get("/usuario/{usuario_id}", response_model=schemas.PageHistoricoOut,
        summary="Listar histórico de um usuário",
        description="Somente adim ou bibliotecário podem listar histórico de um usuário qualquer."
)
def historico_por_usuario(usuario_id: int, skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=100),
        db: Session = Depends(get_db),
        _ = Depends(exigir_roles("admin", "bibliotecario"))):
    return historico_service.listar_historico_usuario_service(
        db=db,
        usuario_id=usuario_id,
        skip=skip,
        limit=limit
    )


# Histórico geral do sistema com base em devoluções
@router.get("/", response_model=schemas.PageHistoricoOut,
        summary="Histórico geral do sistema",
        description="Somente admin ou bibliotecário pode listar histórico geral do sistema."
)
def historico_geral(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=200),
        db: Session = Depends(get_db),
        _ = Depends(exigir_roles("admin", "bibliotecario"))):
    return historico_service.listar_historico_geral_service(
        db=db,
        skip=skip,
        limit=limit
    )
