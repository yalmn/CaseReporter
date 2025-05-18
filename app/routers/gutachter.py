from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/gutachter", tags=["gutachter"])

@router.post("/", response_model=schemas.Gutachter, status_code=201)
async def create_gutachter(
    gutachter: schemas.GutachterCreate,
    db: Session = Depends(database.get_db)
):
    return crud.create_gutachter(db, gutachter)

@router.get("/{gutachter_id}", response_model=schemas.Gutachter)
async def read_gutachter(
    gutachter_id: int,
    db: Session = Depends(database.get_db)
):
    db_g = crud.get_gutachter(db, gutachter_id)
    if not db_g:
        raise HTTPException(status_code=404, detail="Gutachter nicht gefunden")
    return db_g