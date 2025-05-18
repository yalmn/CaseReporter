from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/faelle/{fall_id}/beweismittel", tags=["beweismittel"])

@router.get("/", response_model=list[schemas.Beweismittel])
async def get_items(
    fall_id: int = Path(..., description="ID des Falls"),
    db: Session = Depends(database.get_db)
):
    return crud.get_beweismittel(db, fall_id)

@router.post("/", response_model=schemas.Beweismittel, status_code=201)
async def add_item(
    fall_id: int,
    item: schemas.BeweismittelCreate,
    db: Session = Depends(database.get_db)
):
    from ..crud import get_fall
    if not get_fall(db, fall_id):
        raise HTTPException(status_code=404, detail="Fall nicht gefunden")
    return crud.create_beweismittel(db, fall_id, item)