from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramSemester, ProgramCourse, Course
from schemas import ProgramCourseCreate, ProgramCourseOut


router = APIRouter(
    prefix="/programs/{program_id}/courses",
    tags=["Program Courses"]
)


@router.get("/", response_model=list[ProgramCourseOut])
def get_program_courses(program_id: int, db: Session = Depends(get_db)):
    # ProgramCourse has no direct program_id — it only links to a program
    # through semester_id, so this joins through ProgramSemester.
    return (
        db.query(ProgramCourse)
        .join(ProgramSemester, ProgramCourse.semester_id == ProgramSemester.id)
        .filter(ProgramSemester.program_id == program_id)
        .order_by(ProgramCourse.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramCourseOut)
def add_program_course(
    program_id: int,
    data: ProgramCourseCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    semester = db.get(ProgramSemester, data.semester_id)
    if not semester or semester.program_id != program_id:
        raise HTTPException(status_code=404, detail="Semester not found for this program")

    if not db.get(Course, data.course_id):
        raise HTTPException(status_code=404, detail="Course code not found in catalog")

    row = ProgramCourse(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{program_course_id}")
def delete_program_course(program_id: int, program_course_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(ProgramCourse)
        .join(ProgramSemester, ProgramCourse.semester_id == ProgramSemester.id)
        .filter(ProgramCourse.id == program_course_id, ProgramSemester.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Program course entry not found")

    db.delete(row)
    db.commit()
    return {"message": "Program course entry deleted successfully"}
