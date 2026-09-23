from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramGraduationCriteria
from schemas import ProgramGraduationCriteriaCreate, ProgramGraduationCriteriaOut


router = APIRouter(
    prefix="/programs/{program_id}/graduation-criteria",
    tags=["Program Graduation Criteria"]
)


@router.get("/", response_model=list[ProgramGraduationCriteriaOut])
def get_graduation_criteria(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProgramGraduationCriteria)
        .filter(ProgramGraduationCriteria.program_id == program_id)
        .order_by(ProgramGraduationCriteria.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramGraduationCriteriaOut)
def add_graduation_criterion(
    program_id: int,
    data: ProgramGraduationCriteriaCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = ProgramGraduationCriteria(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{criterion_id}")
def delete_graduation_criterion(program_id: int, criterion_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(ProgramGraduationCriteria)
        .filter(ProgramGraduationCriteria.id == criterion_id, ProgramGraduationCriteria.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Graduation criterion not found")

    db.delete(row)
    db.commit()
    return {"message": "Graduation criterion deleted successfully"}
