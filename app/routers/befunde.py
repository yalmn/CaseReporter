from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/faelle/{fall_id}/befunde", tags=["befunde"])

@router.get("/", response_model=list[schemas.Befund])
async def get_befunde(
    fall_id: int = Path(..., description="ID des Falls"),
    db: Session = Depends(database.get_db)
):
    return crud.get_befunde(db, fall_id)

@router.post("/", response_model=schemas.Befund, status_code=201)
async def add_befund(
    fall_id: int,
    befund: schemas.BefundCreate,
    db: Session = Depends(database.get_db)
):

    from ..crud import get_fall
    if not get_fall(db, fall_id):
        raise HTTPException(status_code=404, detail="Fall nicht gefunden")
    return crud.create_befund(db, fall_id, befund)