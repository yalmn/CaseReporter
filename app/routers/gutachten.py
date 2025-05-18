from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/faelle/{fall_id}/gutachten", tags=["gutachten"])

@router.get("/", response_model=schemas.Gutachten)
async def get_gutachten(
    fall_id: int = Path(..., description="ID des Falls"),
    db: Session = Depends(database.get_db)
):
    db_gt = crud.get_gutachten_by_case(db, fall_id)
    if not db_gt:
        raise HTTPException(status_code=404, detail="Gutachten nicht gefunden")
    return db_gt

@router.post("/", response_model=schemas.Gutachten, status_code=201)
async def create_gutachten(
    fall_id: int,
    gutachten: schemas.GutachtenCreate,
    db: Session = Depends(database.get_db)
):
    from ..crud import get_fall
    if not get_fall(db, fall_id):
        raise HTTPException(status_code=404, detail="Fall nicht gefunden")
    return crud.create_gutachten(db, fall_id, gutachten)