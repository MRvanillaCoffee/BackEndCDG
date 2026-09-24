from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramSemester
from schemas import ProgramSemesterCreate, ProgramSemesterOut


router = APIRouter(
    prefix="/programs/{program_id}/semesters",
    tags=["Program Semesters"]
)


@router.get("/", response_model=list[ProgramSemesterOut])
def get_semesters(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProgramSemester)
        .filter(ProgramSemester.program_id == program_id)
        .order_by(ProgramSemester.year, ProgramSemester.term)
        .all()
    )


@router.post("/", response_model=ProgramSemesterOut)
def add_semester(
    program_id: int,
    data: ProgramSemesterCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = ProgramSemester(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{semester_id}")
def delete_semester(program_id: int, semester_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(ProgramSemester)
        .filter(ProgramSemester.id == semester_id, ProgramSemester.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Semester not found")

    db.delete(row)
    db.commit()
    return {"message": "Semester deleted successfully"}
