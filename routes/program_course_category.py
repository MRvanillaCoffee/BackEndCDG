from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, CourseCategory
from schemas import CourseCategoryCreate, CourseCategoryOut


router = APIRouter(
    prefix="/programs/{program_id}/course-categories",
    tags=["Course Categories"]
)


# Returned as a flat list with parent_id set on each row — the frontend
# reconstructs the tree from that rather than the API nesting it, since
# the UI already builds trees from flat data structures.
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

    if data.parent_id is not None:
        parent = db.get(CourseCategory, data.parent_id)
        if not parent or parent.program_id != program_id:
            raise HTTPException(status_code=404, detail="Parent category not found for this program")

    row = CourseCategory(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.put("/{category_id}", response_model=CourseCategoryOut)
def update_course_category(
    program_id: int,
    category_id: int,
    data: CourseCategoryCreate,
    db: Session = Depends(get_db)
):
    row = (
        db.query(CourseCategory)
        .filter(CourseCategory.id == category_id, CourseCategory.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Course category not found")

    if data.parent_id is not None:
        if data.parent_id == category_id:
            raise HTTPException(status_code=400, detail="A category cannot be its own parent")
        parent = db.get(CourseCategory, data.parent_id)
        if not parent or parent.program_id != program_id:
            raise HTTPException(status_code=404, detail="Parent category not found for this program")

    for field, value in data.model_dump().items():
        setattr(row, field, value)

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

    # Cascades to children (self-referencing FK) and to any course
    # assignments under this category, per the model's cascade config.
    db.delete(row)
    db.commit()
    return {"message": "Course category deleted successfully"}
