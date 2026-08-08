from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramCareer
from schemas import ProgramCareerCreate, ProgramCareerOut


router = APIRouter(
    prefix="/programs/{program_id}/careers",
    tags=["Program Careers"]
)


@router.get("/", response_model=list[ProgramCareerOut])
def get_careers(
    program_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(ProgramCareer)
        .filter(ProgramCareer.program_id == program_id)
        .order_by(ProgramCareer.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramCareerOut)
def add_career(
    program_id: int,
    data: ProgramCareerCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    career = ProgramCareer(
        program_id=program_id,
        **data.model_dump()
    )

    db.add(career)
    db.commit()
    db.refresh(career)

    return career


@router.delete("/{career_id}")
def delete_career(
    program_id: int,
    career_id: int,
    db: Session = Depends(get_db)
):
    career = (
        db.query(ProgramCareer)
        .filter(
            ProgramCareer.id == career_id,
            ProgramCareer.program_id == program_id
        )
        .first()
    )

    if not career:
        raise HTTPException(
            status_code=404,
            detail="Career not found"
        )

    db.delete(career)
    db.commit()

    return {
        "message": "Career deleted successfully"
    }
