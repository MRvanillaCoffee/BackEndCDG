from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, CourseCategory
from schemas import CourseCategoryCreate, CourseCategoryOut


router = APIRouter(
    prefix="/programs/{program_id}/course-categories",
    tags=["Course Categories"]
)


@router.get("/", response_model=list[CourseCategoryOut])
def get_course_categories(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(CourseCategory)
        .filter(CourseCategory.program_id == program_id)
        .order_by(CourseCategory.sort_order)
        .all()
    )


@router.post("/", response_model=CourseCategoryOut)
def add_course_category(
    program_id: int,
    data: CourseCategoryCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = CourseCategory(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{category_id}")
def delete_course_category(program_id: int, category_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(CourseCategory)
        .filter(CourseCategory.id == category_id, CourseCategory.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Course category not found")

    db.delete(row)
    db.commit()
    return {"message": "Course category deleted successfully"}
