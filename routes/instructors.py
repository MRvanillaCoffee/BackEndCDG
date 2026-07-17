from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from database import engine

router = APIRouter(prefix='/instructors',tags=['Instructors'])

# @router.get("/")
# def get_instructor():
#     with engine.connect() as conn:
#         result = conn.execute(text('Select * from instructor'))
#         instructors = [dict(row._mapping) for row in result]

#     return instructors

@router.get("/")
def get_instructor():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM instructor"))
            instructors = [dict(row._mapping) for row in result]

        return instructors

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))