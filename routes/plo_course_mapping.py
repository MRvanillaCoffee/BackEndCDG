from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, Plo, Course, PloCourseMapping
from schemas import PloCourseMappingCreate, PloCourseMappingOut


router = APIRouter(
    prefix="/programs/{program_id}/plo-course-mapping",
    tags=["PLO Course Mapping"]
)


@router.get("/", response_model=list[PloCourseMappingOut])
def get_plo_course_mapping(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(PloCourseMapping)
        .filter(PloCourseMapping.program_id == program_id)
        .all()
    )


@router.post("/", response_model=PloCourseMappingOut)
def add_plo_course_mapping(
    program_id: int,
    data: PloCourseMappingCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    plo = db.get(Plo, data.plo_id)
    if not plo or plo.program_id != program_id:
        raise HTTPException(status_code=404, detail="PLO not found for this program")

    if not db.get(Course, data.course_id):
        raise HTTPException(status_code=404, detail="Course code not found in catalog")

    row = PloCourseMapping(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{mapping_id}")
def delete_plo_course_mapping(program_id: int, mapping_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(PloCourseMapping)
        .filter(PloCourseMapping.id == mapping_id, PloCourseMapping.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="PLO-course mapping not found")

    db.delete(row)
    db.commit()
    return {"message": "PLO-course mapping deleted successfully"}
