from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, Ylo
from schemas import YloCreate, YloOut


router = APIRouter(
    prefix="/programs/{program_id}/ylo",
    tags=["Program YLO"]
)


@router.get("/", response_model=list[YloOut])
def get_ylo(
    program_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(Ylo)
        .filter(Ylo.program_id == program_id)
        .order_by(Ylo.branch, Ylo.year)
        .all()
    )


@router.post("/", response_model=YloOut)
def add_ylo(
    program_id: int,
    data: YloCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    ylo = Ylo(
        program_id=program_id,
        **data.model_dump()
    )

    db.add(ylo)
    db.commit()
    db.refresh(ylo)

    return ylo


@router.delete("/{ylo_id}")
def delete_ylo(
    program_id: int,
    ylo_id: int,
    db: Session = Depends(get_db)
):
    ylo = (
        db.query(Ylo)
        .filter(
            Ylo.id == ylo_id,
            Ylo.program_id == program_id
        )
        .first()
    )

    if not ylo:
        raise HTTPException(
            status_code=404,
            detail="YLO entry not found"
        )

    db.delete(ylo)
    db.commit()

    return {
        "message": "YLO entry deleted successfully"
    }
