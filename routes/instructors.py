from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter(prefix='/instructors',tags=['Instructors'])

@router.get("/")
def get_instructor():
    with engine.connect() as conn:
        result = conn.execute(text('Select * from instructor'))
        instructors = [dict(row._mapping) for row in result]
        
    return instructors
