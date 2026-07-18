from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import Program
from schemas import ProgramCreate, ProgramUpdate, ProgramOut

router = APIRouter(prefix="/api/programs", tags=["programs"])


@router.post("", response_model=ProgramOut, status_code=201)
def create_program(payload: ProgramCreate, db: Session = Depends(get_db)):
    program = Program(**payload.model_dump())
    db.add(program)
    db.commit()
    db.refresh(program)
    return program


@router.get("", response_model=list[ProgramOut])
def list_programs(db: Session = Depends(get_db)):
    result = db.execute(select(Program).order_by(Program.id.desc()))
    return result.scalars().all()


@router.get("/{program_id}", response_model=ProgramOut)
def get_program(program_id: int, db: Session = Depends(get_db)):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(404, "Program not found")
    return program


@router.patch("/{program_id}", response_model=ProgramOut)
def update_program(program_id: int, payload: ProgramUpdate, db: Session = Depends(get_db)):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(404, "Program not found")

    # เฉพาะ field ที่ user ส่งมาจริงเท่านั้น (partial update)
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(program, key, value)

    db.commit()
    db.refresh(program)
    return program


@router.delete("/{program_id}", status_code=204)
def delete_program(program_id: int, db: Session = Depends(get_db)):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(404, "Program not found")
    db.delete(program)
    db.commit()