from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramEvaluationProcess
from schemas import ProgramEvaluationProcessCreate, ProgramEvaluationProcessOut


router = APIRouter(
    prefix="/programs/{program_id}/evaluation-process",
    tags=["Program Evaluation Process"]
)


@router.get("/", response_model=list[ProgramEvaluationProcessOut])
def get_evaluation_process(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProgramEvaluationProcess)
        .filter(ProgramEvaluationProcess.program_id == program_id)
        .order_by(ProgramEvaluationProcess.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramEvaluationProcessOut)
def add_evaluation_process(
    program_id: int,
    data: ProgramEvaluationProcessCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = ProgramEvaluationProcess(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{item_id}")
def delete_evaluation_process(program_id: int, item_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(ProgramEvaluationProcess)
        .filter(ProgramEvaluationProcess.id == item_id, ProgramEvaluationProcess.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Evaluation process item not found")

    db.delete(row)
    db.commit()
    return {"message": "Evaluation process item deleted successfully"}
