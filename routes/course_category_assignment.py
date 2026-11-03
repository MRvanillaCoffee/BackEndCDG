from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, CourseCategory, Course, CourseCategoryAssignment
from schemas import CourseCategoryAssignmentCreate, CourseCategoryAssignmentOut


router = APIRouter(
    prefix="/programs/{program_id}/category-assignments",
    tags=["Course Category Assignments"]
)


@router.get("/", response_model=list[CourseCategoryAssignmentOut])
def get_category_assignments(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(CourseCategoryAssignment)
        .filter(CourseCategoryAssignment.program_id == program_id)
        .order_by(CourseCategoryAssignment.sort_order)
        .all()
    )


@router.post("/", response_model=CourseCategoryAssignmentOut)
def add_category_assignment(
    program_id: int,
    data: CourseCategoryAssignmentCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    category = db.get(CourseCategory, data.category_id)
    if not category or category.program_id != program_id:
        raise HTTPException(status_code=404, detail="Category not found for this program")

    if not db.get(Course, data.course_id):
        raise HTTPException(status_code=404, detail="Course code not found in catalog")

    row = CourseCategoryAssignment(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{assignment_id}")
def delete_category_assignment(program_id: int, assignment_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(CourseCategoryAssignment)
        .filter(CourseCategoryAssignment.id == assignment_id, CourseCategoryAssignment.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Category assignment not found")

    db.delete(row)
    db.commit()
    return {"message": "Category assignment deleted successfully"}
