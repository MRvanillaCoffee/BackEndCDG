from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramInstructor
from schemas import ProgramInstructorCreate, ProgramInstructorOut


router = APIRouter(
    prefix="/programs/{program_id}/instructors",
    tags=["Program Instructors"]
)


@router.get("/", response_model=list[ProgramInstructorOut])
def get_instructors(
    program_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(ProgramInstructor)
        .filter(
            ProgramInstructor.program_id == program_id
        )
        .order_by(ProgramInstructor.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramInstructorOut)
def add_instructor(
    program_id: int,
    data: ProgramInstructorCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    instructor = ProgramInstructor(
        program_id=program_id,
        **data.model_dump()
    )

    db.add(instructor)
    db.commit()
    db.refresh(instructor)

    return instructor


@router.delete("/{instructor_id}")
def delete_instructor(
    program_id: int,
    instructor_id: int,
    db: Session = Depends(get_db)
):
    instructor = (
        db.query(ProgramInstructor)
        .filter(
            ProgramInstructor.id == instructor_id,
            ProgramInstructor.program_id == program_id
        )
        .first()
    )

    if not instructor:
        raise HTTPException(
            status_code=404,
            detail="Instructor not found"
        )

    db.delete(instructor)
    db.commit()

    return {
        "message": "Instructor deleted successfully"
    }
