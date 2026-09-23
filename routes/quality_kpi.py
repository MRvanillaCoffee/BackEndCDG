from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, QualityKpi
from schemas import QualityKpiCreate, QualityKpiOut


router = APIRouter(
    prefix="/programs/{program_id}/quality-kpis",
    tags=["Quality KPIs"]
)


@router.get("/", response_model=list[QualityKpiOut])
def get_quality_kpis(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(QualityKpi)
        .filter(QualityKpi.program_id == program_id)
        .all()
    )


@router.post("/", response_model=QualityKpiOut)
def add_quality_kpi(
    program_id: int,
    data: QualityKpiCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = QualityKpi(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{kpi_id}")
def delete_quality_kpi(program_id: int, kpi_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(QualityKpi)
        .filter(QualityKpi.id == kpi_id, QualityKpi.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="KPI not found")

    db.delete(row)
    db.commit()
    return {"message": "KPI deleted successfully"}
