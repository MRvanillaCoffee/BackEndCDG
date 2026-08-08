from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramApproval
from schemas import ProgramApprovalCreate, ProgramApprovalOut


router = APIRouter(
    prefix="/programs/{program_id}/approvals",
    tags=["Program Approvals"]
)


@router.get("/", response_model=list[ProgramApprovalOut])
def get_approvals(
    program_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(ProgramApproval)
        .filter(ProgramApproval.program_id == program_id)
        .order_by(ProgramApproval.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramApprovalOut)
def add_approval(
    program_id: int,
    data: ProgramApprovalCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    approval = ProgramApproval(
        program_id=program_id,
        **data.model_dump()
    )

    db.add(approval)
    db.commit()
    db.refresh(approval)

    return approval


@router.delete("/{approval_id}")
def delete_approval(
    program_id: int,
    approval_id: int,
    db: Session = Depends(get_db)
):
    approval = (
        db.query(ProgramApproval)
        .filter(
            ProgramApproval.id == approval_id,
            ProgramApproval.program_id == program_id
        )
        .first()
    )

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    db.delete(approval)
    db.commit()

    return {
        "message": "Approval deleted successfully"
    }
