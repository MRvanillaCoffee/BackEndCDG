from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, Course, CourseInstructor
from schemas import CourseInstructorCreate, CourseInstructorOut


router = APIRouter(
    prefix="/programs/{program_id}/course-instructors",
    tags=["Course Instructors"]
)


@router.get("/", response_model=list[CourseInstructorOut])
def get_course_instructors(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(CourseInstructor)
        .filter(CourseInstructor.program_id == program_id)
        .order_by(CourseInstructor.sort_order)
        .all()
    )


@router.post("/", response_model=CourseInstructorOut)
def add_course_instructor(
    program_id: int,
    data: CourseInstructorCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    if not db.get(Course, data.course_id):
        raise HTTPException(status_code=404, detail="Course code not found in catalog")

    row = CourseInstructor(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{assignment_id}")
def delete_course_instructor(program_id: int, assignment_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(CourseInstructor)
        .filter(CourseInstructor.id == assignment_id, CourseInstructor.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Course instructor assignment not found")

    db.delete(row)
    db.commit()
    return {"message": "Course instructor assignment deleted successfully"}
