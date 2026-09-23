from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramFacultyDevelopment
from schemas import ProgramFacultyDevelopmentCreate, ProgramFacultyDevelopmentOut


router = APIRouter(
    prefix="/programs/{program_id}/faculty-development",
    tags=["Program Faculty Development"]
)


@router.get("/", response_model=list[ProgramFacultyDevelopmentOut])
def get_faculty_development(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProgramFacultyDevelopment)
        .filter(ProgramFacultyDevelopment.program_id == program_id)
        .order_by(ProgramFacultyDevelopment.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramFacultyDevelopmentOut)
def add_faculty_development(
    program_id: int,
    data: ProgramFacultyDevelopmentCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = ProgramFacultyDevelopment(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{item_id}")
def delete_faculty_development(program_id: int, item_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(ProgramFacultyDevelopment)
        .filter(ProgramFacultyDevelopment.id == item_id, ProgramFacultyDevelopment.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Faculty development item not found")

    db.delete(row)
    db.commit()
    return {"message": "Faculty development item deleted successfully"}
