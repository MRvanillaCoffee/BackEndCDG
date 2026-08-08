
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program
from schemas import ProgramCreate, ProgramUpdate, ProgramOut


router = APIRouter(
    prefix="/programs",
    tags=["Programs"]
)


# ============================================================
# GET ALL PROGRAMS
# ============================================================

@router.get(
    "/",
    response_model=list[ProgramOut]
)
def get_programs(
    db: Session = Depends(get_db)
):
    programs = (
        db.query(Program)
        .order_by(Program.id.desc())
        .all()
    )

    return programs


# ============================================================
# GET ONE PROGRAM
# ============================================================

@router.get(
    "/{program_id}",
    response_model=ProgramOut
)
def get_program(
    program_id: int,
    db: Session = Depends(get_db)
):
    program = (
        db.query(Program)
        .filter(Program.id == program_id)
        .first()
    )

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    return program


# ============================================================
# CREATE PROGRAM
# ============================================================

@router.post(
    "/",
    response_model=ProgramOut
)
def create_program(
    data: ProgramCreate,
    db: Session = Depends(get_db)
):
    program = Program(
        **data.model_dump()
    )

    db.add(program)
    db.commit()
    db.refresh(program)

    return program


# ============================================================
# UPDATE PROGRAM
# ============================================================

@router.put(
    "/{program_id}",
    response_model=ProgramOut
)
def update_program(
    program_id: int,
    data: ProgramUpdate,
    db: Session = Depends(get_db)
):
    program = (
        db.query(Program)
        .filter(Program.id == program_id)
        .first()
    )

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(program, field, value)

    db.commit()
    db.refresh(program)

    return program


# ============================================================
# DELETE PROGRAM
# ============================================================

@router.delete(
    "/{program_id}"
)
def delete_program(
    program_id: int,
    db: Session = Depends(get_db)
):
    program = (
        db.query(Program)
        .filter(Program.id == program_id)
        .first()
    )

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    db.delete(program)
    db.commit()

    return {
        "message": "Program deleted successfully",
        "program_id": program_id
    }
