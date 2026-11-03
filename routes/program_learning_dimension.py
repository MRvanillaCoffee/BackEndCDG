from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramLearningDimension
from schemas import ProgramLearningDimensionIn, ProgramLearningDimensionOut


router = APIRouter(
    prefix="/programs/{program_id}/learning-dimension",
    tags=["Program Learning Dimension"]
)


@router.get("", response_model=ProgramLearningDimensionOut)
def get_learning_dimension(program_id: int, db: Session = Depends(get_db)):
    record = (
        db.query(ProgramLearningDimension)
        .filter(ProgramLearningDimension.program_id == program_id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Learning dimension not set for this program yet")
    return record


@router.put("", response_model=ProgramLearningDimensionOut)
def upsert_learning_dimension(
    program_id: int,
    data: ProgramLearningDimensionIn,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    record = (
        db.query(ProgramLearningDimension)
        .filter(ProgramLearningDimension.program_id == program_id)
        .first()
    )

    if record:
        for field, value in data.model_dump().items():
            setattr(record, field, value)
    else:
        record = ProgramLearningDimension(program_id=program_id, **data.model_dump())
        db.add(record)

    db.commit()
    db.refresh(record)
    return record
