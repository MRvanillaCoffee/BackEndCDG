from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramLearningAttribute
from schemas import ProgramLearningAttributeCreate, ProgramLearningAttributeOut


router = APIRouter(
    prefix="/programs/{program_id}/learning-attributes",
    tags=["Program Learning Attributes"]
)


@router.get("/", response_model=list[ProgramLearningAttributeOut])
def get_learning_attributes(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProgramLearningAttribute)
        .filter(ProgramLearningAttribute.program_id == program_id)
        .order_by(ProgramLearningAttribute.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramLearningAttributeOut)
def add_learning_attribute(
    program_id: int,
    data: ProgramLearningAttributeCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = ProgramLearningAttribute(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{attribute_id}")
def delete_learning_attribute(program_id: int, attribute_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(ProgramLearningAttribute)
        .filter(ProgramLearningAttribute.id == attribute_id, ProgramLearningAttribute.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Learning attribute not found")

    db.delete(row)
    db.commit()
    return {"message": "Learning attribute deleted successfully"}
