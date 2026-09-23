from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramEvaluation
from schemas import ProgramEvaluationIn, ProgramEvaluationOut


router = APIRouter(
    prefix="/programs/{program_id}/evaluation",
    tags=["Program Evaluation"]
)


@router.get("", response_model=ProgramEvaluationOut)
def get_evaluation(program_id: int, db: Session = Depends(get_db)):
    record = db.query(ProgramEvaluation).filter(ProgramEvaluation.program_id == program_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Evaluation not set for this program yet")
    return record


@router.put("", response_model=ProgramEvaluationOut)
def upsert_evaluation(program_id: int, data: ProgramEvaluationIn, db: Session = Depends(get_db)):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    record = db.query(ProgramEvaluation).filter(ProgramEvaluation.program_id == program_id).first()
    if record:
        for field, value in data.model_dump().items():
            setattr(record, field, value)
    else:
        record = ProgramEvaluation(program_id=program_id, **data.model_dump())
        db.add(record)

    db.commit()
    db.refresh(record)
    return record
