from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import User
from auth import verify_password, create_access_token
from schemas import Token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == form.username)).scalar_one_or_none()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "อีเมลหรือรหัสผ่านไม่ถูกต้อง")
    if not user.is_active:
        raise HTTPException(403, "บัญชีถูกระงับ")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}