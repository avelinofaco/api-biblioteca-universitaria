from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.permissions import exigir_roles

from app import crud, schemas
from app.deps import get_db

router = APIRouter(prefix="/livros", tags=["livros"])

@router.post("/", response_model=schemas.LivroOut, status_code=status.HTTP_201_CREATED, description="So quem pode criar livros sao os adminstradores/bibliotecarios")
def criar_livro(livro_in: schemas.LivroCreate, 
                db: Session = Depends(get_db),
                _ = Depends(exigir_roles("admin","bibliotecario"))):
    livro = crud.criar_livro(
        db,
        titulo=livro_in.titulo,
        autor=livro_in.autor,
        isbn=livro_in.isbn,
        quantidade_total=livro_in.quantidade_total,
        area=livro_in.area
    )
    return livro

@router.get("/", response_model=List[schemas.LivroOut])
def listar_livros(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    # simples: usar query direta via crud (podes criar função se preferir)
    from sqlalchemy import select
    livros = db.execute(select(crud.Livro).offset(skip).limit(limit)).scalars().all()
    return livros

@router.get("/{livro_id}", response_model=schemas.LivroOut)
def recuperar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = crud.get_livro(db, livro_id=livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

@router.put("/{livro_id}", response_model=schemas.LivroOut)
def atualizar_livro(livro_id: int, payload: schemas.LivroUpdate, db: Session = Depends(get_db)):
    livro = crud.get_livro(db, livro_id=livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    # aplica alterações de forma simples
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(livro, field, value)
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro


# Delete livro 
@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT, description="So quem pode remover livros é o admin")
def remover_livro(livro_id: int, db: Session = Depends(get_db), _ = Depends(exigir_roles("admin"))):
    livro = crud.get_livro(db, livro_id=livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(livro)
    db.commit()
    return None
