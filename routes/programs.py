# routers/programs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import Program, ProgramReview, User
from schemas import ProgramCreate, ProgramUpdate, ProgramOut, ReviewIn
from auth import get_current_user, require_role

router = APIRouter(prefix="/api/programs", tags=["programs"])

@router.post(
    "",
    response_model=ProgramOut,
    status_code=201,
    dependencies=[Depends(require_role("admin", "coordinator"))],
)
def create_program(
    payload: ProgramCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    program = Program(**payload.model_dump(), created_by=user.id)
    db.add(program)
    db.commit()
    db.refresh(program)
    return program

@router.get("", response_model=list[ProgramOut])
def list_programs(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = select(Program).order_by(Program.id.desc())
    if user.role == "coordinator":
        query = query.where(Program.created_by == user.id)
    return db.execute(query).scalars().all()

@router.get("/{program_id}", response_model=ProgramOut)
def get_program(
    program_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(404, "Program not found")

    if user.role == "coordinator" and program.created_by != user.id:
        raise HTTPException(403, "ไม่มีสิทธิ์ดูหลักสูตรนี้")

    return program

@router.patch("/{program_id}", response_model=ProgramOut)
def update_program(
    program_id: int,
    payload: ProgramUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(404, "Program not found")

    if user.role == "reviewer":
        raise HTTPException(403, "Reviewer ไม่มีสิทธิ์แก้ไขข้อมูล")
    if user.role == "coordinator" and program.created_by != user.id:
        raise HTTPException(403, "แก้ไขได้เฉพาะหลักสูตรของตัวเอง")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(program, key, value)

    db.commit()
    db.refresh(program)
    return program

@router.delete(
    "/{program_id}",
    status_code=204,
    dependencies=[Depends(require_role("admin"))],
)
def delete_program(program_id: int, db: Session = Depends(get_db)):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(404, "Program not found")
    db.delete(program)
    db.commit()


@router.post(
    "/{program_id}/submit",
    response_model=ProgramOut,
    dependencies=[Depends(require_role("admin", "coordinator"))],
)
def submit_program(
    program_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(404, "Program not found")

    if user.role == "coordinator" and program.created_by != user.id:
        raise HTTPException(403, "ส่งตรวจได้เฉพาะหลักสูตรของตัวเอง")

    if program.status not in ("draft", "rejected"):
        raise HTTPException(
            400, f"ไม่สามารถส่งตรวจได้ (สถานะปัจจุบัน: {program.status})"
        )

    program.status = "under_review"
    db.commit()
    db.refresh(program)
    return program

@router.post(
    "/{program_id}/review",
    response_model=ProgramOut,
    dependencies=[Depends(require_role("admin", "reviewer"))],
)
def review_program(
    program_id: int,
    payload: ReviewIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(404, "Program not found")

    if program.status != "under_review":
        raise HTTPException(400, "หลักสูตรนี้ไม่ได้อยู่ระหว่างการตรวจสอบ")

    review = ProgramReview(
        program_id=program_id,
        reviewer_id=user.id,
        decision=payload.decision,
        comment=payload.comment,
    )
    db.add(review)

    if payload.decision == "approved":
        program.status = "approved"
    elif payload.decision == "rejected":
        program.status = "rejected"

    db.commit()
    db.refresh(program)
    return program

@router.get("/{program_id}/reviews")
def list_reviews(
    program_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(404, "Program not found")

    if user.role == "coordinator" and program.created_by != user.id:
        raise HTTPException(403, "ไม่มีสิทธิ์ดูประวัติการตรวจของหลักสูตรนี้")

    result = db.execute(
        select(ProgramReview)
        .where(ProgramReview.program_id == program_id)
        .order_by(ProgramReview.created_at.desc())
    )
    reviews = result.scalars().all()
    return [
        {
            "id": r.id,
            "reviewer_id": r.reviewer_id,
            "decision": r.decision,
            "comment": r.comment,
            "created_at": r.created_at,
        }
        for r in reviews
    ]