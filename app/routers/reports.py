from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..report_service import ReportService
from fastapi.responses import FileResponse

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/{case_id}")
def get_report(case_id: str, db: Session = Depends(get_db)):
    service = ReportService(db)
    try:
        pdf_path, _ = service.create_report(case_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return FileResponse(pdf_path, media_type="application/pdf")

@router.post("/{case_id}/fazit")
def get_fazit(case_id: str, db: Session = Depends(get_db)):
    service = ReportService(db)
    try:
        _, ki_fazit = service.create_report(case_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"ki_fazit": ki_fazit}