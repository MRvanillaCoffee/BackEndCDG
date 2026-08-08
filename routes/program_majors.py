from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramMajor
from schemas import ProgramMajorCreate, ProgramMajorOut


router = APIRouter(
    prefix="/programs/{program_id}/majors",
    tags=["Program Majors"]
)


@router.get("/", response_model=list[ProgramMajorOut])
def get_majors(
    program_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(ProgramMajor)
        .filter(ProgramMajor.program_id == program_id)
        .order_by(ProgramMajor.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramMajorOut)
def add_major(
    program_id: int,
    data: ProgramMajorCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    major = ProgramMajor(
        program_id=program_id,
        **data.model_dump()
    )

    db.add(major)
    db.commit()
    db.refresh(major)

    return major


@router.delete("/{major_id}")
def delete_major(
    program_id: int,
    major_id: int,
    db: Session = Depends(get_db)
):
    major = (
        db.query(ProgramMajor)
        .filter(
            ProgramMajor.id == major_id,
            ProgramMajor.program_id == program_id
        )
        .first()
    )

    if not major:
        raise HTTPException(
            status_code=404,
            detail="Major not found"
        )

    db.delete(major)
    db.commit()

    return {
        "message": "Major deleted successfully"
    }
