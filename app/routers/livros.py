from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.permissions import exigir_roles
from app.services import livro_service
from app.services.exceptions import BusinessRuleError, NotFoundError

from app import schemas
from app.deps import get_db
from app.deps import get_current_user


router = APIRouter(prefix="/livros", tags=["livros"], dependencies=[Depends(get_current_user)]) #ninguém acessa livros sem estar logado

# Criar livro
@router.post("/", response_model=schemas.LivroOut, status_code=status.HTTP_201_CREATED, 
             description="So quem pode criar livros sao os adminstradores ou bibliotecarios")
def criar_livro(livro_in: schemas.LivroCreate,   #rota espera um LivroCreate(validação do corpo)
                db: Session = Depends(get_db),   # Tem dependencia com seesao BD
                _ = Depends(exigir_roles("admin","bibliotecario"))): #Regra de autorização
    return livro_service.criar_livro_service(db, livro_in)   # retorna um LivroOut

# Listar livros
@router.get("/", response_model=schemas.PageLivro, description="Toso usuarios podem ver livros")
def listar_livros(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return livro_service.listar_livros_service(db, skip, limit)


# Recuperar livro por ID
@router.get("/{livro_id}", response_model=schemas.LivroOut)
def recuperar_livro(livro_id: int, db: Session = Depends(get_db)):
    try:
        return livro_service.recuperar_livro_service(db, livro_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Atualizar livro 
@router.patch("/{livro_id}", response_model=schemas.LivroOut, description="Somente admin ou bibliotecario pode atualizar livros")
def atualizar_livro(livro_id: int, payload: schemas.LivroUpdate, 
                    db: Session = Depends(get_db),
                    _ = Depends(exigir_roles("admin","bibliotecario"))):
    try:
        return livro_service.atualizar_livro_service(
            db,
            livro_id,
            payload.model_dump(exclude_unset=True)
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BusinessRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Delete livro 
# Remover livro
@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT,
                description="Somente admin pode remover livros")
def remover_livro(livro_id: int, db: Session = Depends(get_db),  _ = Depends(exigir_roles("admin"))):
    try:
        livro_service.remover_livro_service(db, livro_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BusinessRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return None

