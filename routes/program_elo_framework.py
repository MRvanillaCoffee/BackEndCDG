from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramEloFramework
from schemas import ProgramEloFrameworkIn, ProgramEloFrameworkOut


router = APIRouter(
    prefix="/programs/{program_id}/elo-framework",
    tags=["Program ELO Framework"]
)


@router.get("", response_model=ProgramEloFrameworkOut)
def get_elo_framework(
    program_id: int,
    db: Session = Depends(get_db)
):
    record = (
        db.query(ProgramEloFramework)
        .filter(ProgramEloFramework.program_id == program_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="ELO framework not set for this program yet"
        )

    return record


@router.put("", response_model=ProgramEloFrameworkOut)
def upsert_elo_framework(
    program_id: int,
    data: ProgramEloFrameworkIn,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    record = (
        db.query(ProgramEloFramework)
        .filter(ProgramEloFramework.program_id == program_id)
        .first()
    )

    if record:
        record.framework = data.framework
    else:
        record = ProgramEloFramework(
            program_id=program_id,
            framework=data.framework
        )
        db.add(record)

    db.commit()
    db.refresh(record)

    return record
