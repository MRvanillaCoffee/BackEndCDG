from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramFavorite, User
from schemas import ProgramFavoriteOut


router = APIRouter(
    prefix="/programs/{program_id}/favorites",
    tags=["Program Favorites"]
)


class FavoriteIn(BaseModel):
    user_id: int


@router.get("/", response_model=list[ProgramFavoriteOut])
def get_favorites(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProgramFavorite)
        .filter(ProgramFavorite.program_id == program_id)
        .all()
    )


@router.post("/", response_model=ProgramFavoriteOut)
def star_program(
    program_id: int,
    data: FavoriteIn,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    if not db.get(User, data.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    existing = (
        db.query(ProgramFavorite)
        .filter(ProgramFavorite.program_id == program_id, ProgramFavorite.user_id == data.user_id)
        .first()
    )
    if existing:
        return existing  # starring an already-starred program is a no-op, not an error

    row = ProgramFavorite(program_id=program_id, user_id=data.user_id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{user_id}")
def unstar_program(program_id: int, user_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(ProgramFavorite)
        .filter(ProgramFavorite.program_id == program_id, ProgramFavorite.user_id == user_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="This program isn't starred by this user")

    db.delete(row)
    db.commit()
    return {"message": "Program unstarred successfully"}
