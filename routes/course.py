from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from database import get_db
from models import Course, CoursePrerequisite, CourseCorequisite
from schemas import CourseCreate, CourseOut


router = APIRouter(
    prefix="/courses",
    tags=["Course Catalog"]
)


def _load(db: Session, course_id: str) -> Course | None:
    return (
        db.query(Course)
        .options(selectinload(Course.prerequisites), selectinload(Course.corequisites))
        .filter(Course.id == course_id)
        .first()
    )


def _to_out(course: Course) -> CourseOut:
    return CourseOut(
        id=course.id,
        name_th=course.name_th,
        name_en=course.name_en,
        credits=course.credits,
        credit_total=course.credit_total,
        credit_lecture=course.credit_lecture,
        credit_lab=course.credit_lab,
        credit_selfstudy=course.credit_selfstudy,
        description_th=course.description_th,
        description_en=course.description_en,
        prereq=course.prereq,
        note=course.note,
        created_by=course.created_by,
        prerequisites=[p.prerequisite_course_id for p in course.prerequisites],
        corequisites=[c.corequisite_course_id for c in course.corequisites]
    )


def _sync_links(db: Session, course: Course, data: CourseCreate):
    # Wipe and re-add — same pattern used elsewhere for small child lists.
    db.query(CoursePrerequisite).filter(CoursePrerequisite.course_id == course.id).delete()
    db.query(CourseCorequisite).filter(CourseCorequisite.course_id == course.id).delete()

    for code in data.prerequisites:
        if not db.get(Course, code):
            raise HTTPException(status_code=404, detail=f"Prerequisite course '{code}' not found in catalog")
        db.add(CoursePrerequisite(course_id=course.id, prerequisite_course_id=code))

    for code in data.corequisites:
        if not db.get(Course, code):
            raise HTTPException(status_code=404, detail=f"Corequisite course '{code}' not found in catalog")
        db.add(CourseCorequisite(course_id=course.id, corequisite_course_id=code))


@router.get("/", response_model=list[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    courses = (
        db.query(Course)
        .options(selectinload(Course.prerequisites), selectinload(Course.corequisites))
        .order_by(Course.id)
        .all()
    )
    return [_to_out(c) for c in courses]


@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: str, db: Session = Depends(get_db)):
    course = _load(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return _to_out(course)


@router.post("/", response_model=CourseOut)
def create_course(data: CourseCreate, db: Session = Depends(get_db)):
    if db.get(Course, data.id):
        raise HTTPException(status_code=409, detail="A course with this code already exists")

    course = Course(**data.model_dump(exclude={"prerequisites", "corequisites"}))
    db.add(course)
    db.flush()  # course.id is already set (it's client-supplied), but ensures the row exists before linking

    try:
        _sync_links(db, course, data)
    except HTTPException:
        db.rollback()  # undo the flushed course row too, not just the failed link
        raise

    db.commit()
    course = _load(db, course.id)
    return _to_out(course)


@router.put("/{course_id}", response_model=CourseOut)
def update_course(course_id: str, data: CourseCreate, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    update_data = data.model_dump(exclude={"id", "prerequisites", "corequisites"})
    for field, value in update_data.items():
        setattr(course, field, value)

    try:
        _sync_links(db, course, data)
    except HTTPException:
        db.rollback()
        raise

    db.commit()
    course = _load(db, course_id)
    return _to_out(course)


@router.delete("/{course_id}")
def delete_course(course_id: str, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}
