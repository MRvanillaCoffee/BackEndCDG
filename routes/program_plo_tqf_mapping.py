from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, PloTqfMapping
from schemas import PloTqfMappingCreate, PloTqfMappingOut


router = APIRouter(
    prefix="/programs/{program_id}/plo-tqf-mapping",
    tags=["Program PLO TQF Mapping"]
)


@router.get("/", response_model=list[PloTqfMappingOut])
def get_plo_tqf_mapping(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(PloTqfMapping)
        .filter(PloTqfMapping.program_id == program_id)
        .all()
    )


@router.post("/", response_model=PloTqfMappingOut)
def add_plo_tqf_mapping(program_id: int, data: PloTqfMappingCreate, db: Session = Depends(get_db)):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = PloTqfMapping(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{mapping_id}")
def delete_plo_tqf_mapping(program_id: int, mapping_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(PloTqfMapping)
        .filter(PloTqfMapping.id == mapping_id, PloTqfMapping.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="PLO-TQF mapping not found")

    db.delete(row)
    db.commit()
    return {"message": "PLO-TQF mapping deleted successfully"}
