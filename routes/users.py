from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import User
from schemas import UserCreate, UserOut
from auth import hash_password, require_role,get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    return user

@router.post("", response_model=UserOut, status_code=201, dependencies=[Depends(require_role("admin"))])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(400, "อีเมลนี้ถูกใช้แล้ว")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("", response_model=list[UserOut], dependencies=[Depends(require_role("admin"))])
def list_users(db: Session = Depends(get_db)):
    return db.execute(select(User)).scalars().all()