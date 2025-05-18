from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/faelle", tags=["faelle"])

@router.post("/", response_model=schemas.Fall)
async def create_fall(
    fall: schemas.FallCreate, db: Session = Depends(database.get_db)
):
    if crud.get_fall(db, fall.fall_id):
        raise HTTPException(status_code=400, detail="Fall existiert bereits")
    return crud.create_fall(db, fall)

@router.get("/{fall_id}", response_model=schemas.Fall)
async def read_fall(
    fall_id: str, db: Session = Depends(database.get_db)
):
    db_fall = crud.get_fall(db, fall_id)
    if not db_fall:
        raise HTTPException(status_code=404, detail="Fall nicht gefunden")
    return db_fall