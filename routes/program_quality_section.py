from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramQualitySection
from schemas import ProgramQualitySectionCreate, ProgramQualitySectionOut


router = APIRouter(
    prefix="/programs/{program_id}/quality-sections",
    tags=["Program Quality Sections"]
)


@router.get("/", response_model=list[ProgramQualitySectionOut])
def get_quality_sections(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProgramQualitySection)
        .filter(ProgramQualitySection.program_id == program_id)
        .order_by(ProgramQualitySection.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramQualitySectionOut)
def add_quality_section(
    program_id: int,
    data: ProgramQualitySectionCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = ProgramQualitySection(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{section_id}")
def delete_quality_section(program_id: int, section_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(ProgramQualitySection)
        .filter(ProgramQualitySection.id == section_id, ProgramQualitySection.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Quality section not found")

    db.delete(row)
    db.commit()
    return {"message": "Quality section deleted successfully"}
