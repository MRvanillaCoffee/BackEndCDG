from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, Plo
from schemas import PloCreate, PloOut


router = APIRouter(
    prefix="/programs/{program_id}/plo",
    tags=["Program PLO"]
)


@router.get("/", response_model=list[PloOut])
def get_plo(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Plo)
        .filter(Plo.program_id == program_id)
        .order_by(Plo.sort_order)
        .all()
    )


@router.post("/", response_model=PloOut)
def add_plo(program_id: int, data: PloCreate, db: Session = Depends(get_db)):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = Plo(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{plo_id}")
def delete_plo(program_id: int, plo_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(Plo)
        .filter(Plo.id == plo_id, Plo.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="PLO not found")

    db.delete(row)
    db.commit()
    return {"message": "PLO deleted successfully"}
