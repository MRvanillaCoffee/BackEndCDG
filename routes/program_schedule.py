from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramSchedule
from schemas import ProgramScheduleCreate, ProgramScheduleOut


router = APIRouter(
    prefix="/programs/{program_id}/schedule",
    tags=["Program Schedule"]
)


@router.get("/", response_model=list[ProgramScheduleOut])
def get_schedule(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProgramSchedule)
        .filter(ProgramSchedule.program_id == program_id)
        .all()
    )


@router.post("/", response_model=ProgramScheduleOut)
def add_schedule(
    program_id: int,
    data: ProgramScheduleCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = ProgramSchedule(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{schedule_id}")
def delete_schedule(program_id: int, schedule_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(ProgramSchedule)
        .filter(
            ProgramSchedule.id == schedule_id,
            ProgramSchedule.program_id == program_id
        )
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Schedule entry not found")

    db.delete(row)
    db.commit()
    return {"message": "Schedule entry deleted successfully"}
