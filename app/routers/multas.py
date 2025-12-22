from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.services.exceptions import NotFoundError

from app import models, schemas
from app.deps import get_db, get_current_user
from app.services import multa_service
from app.dependencies.permissions import exigir_roles

router = APIRouter(prefix="/multas", tags=["multas"])

# Listar todas as multas (admin / bibliotecário)
@router.get("/", response_model=schemas.PageMulta,
        summary="Listar todas as multas",
        description="Bibliotecário e admin podem listar todas as multas do sistema.")
def listar_multas(skip: int = 0, limit: int = 50,
        db: Session = Depends(get_db),
        _ = Depends(exigir_roles("bibliotecario", "admin"))):
    return multa_service.listar_multas_service(db, skip, limit)


# Listar multas de um usuário específico (admin / bibliotecário)
@router.get("/usuario/{usuario_id}", response_model=schemas.PageMulta,
        summary="Listar multas de um usuário",
        description="Quais multas pertencem a esse usuário. Admin e bibliotecário podem listar multas de um usuário específico.")
def multas_do_usuario(usuario_id: int, skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        _ = Depends(exigir_roles("admin", "bibliotecario"))):
    return multa_service.listar_multas_usuario_service(
        db=db, 
        usuario_id=usuario_id, 
        skip=skip, 
        limit=limit
    )


# Listar multas do usuário logado
@router.get("/me", response_model=schemas.PageMulta,
        summary="Listar minhas multas",
        description="Usuario logado pode listar suas multas.")
def minhas_multas(skip: int = 0, limit: int = 10,
        db: Session = Depends(get_db),
        usuario_logado: models.Usuario = Depends(get_current_user)):
    return multa_service.listar_minhas_multas_service(
        db=db,
        usuario_id=usuario_logado.id,
        skip=skip,
        limit=limit
    )


# Buscar multa por ID (admin / bibliotecário)
@router.get("/{multa_id}", response_model=schemas.MultaOut,
        summary="Buscar multa especifica por ID",
        description="Quero essa multa específica, não importa de quem seja. Admin e bibliotecário podem buscar uma multa por ID. ")
def recuperar_multa(multa_id: int, db: Session = Depends(get_db), _ = Depends(exigir_roles("admin", "bibliotecario"))):
    try:
        return multa_service.recuperar_multa_service(db, multa_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# Pagar multa (aluno)
@router.post("/{multa_id}/pagar", response_model=schemas.MultaOut,
        summary="Pagar multa",
        description="Usuario logado pode pagar sua multa.")
def pagar_multa(multa_id: int, db: Session = Depends(get_db), usuario_logado: models.Usuario = Depends(get_current_user)):
    try:
        return multa_service.pagar_multa_service(
            db=db,
            multa_id=multa_id,
            usuario_id=usuario_logado.id
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

