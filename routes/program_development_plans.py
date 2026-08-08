from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramDevelopmentPlan
from schemas import ProgramDevelopmentPlanCreate, ProgramDevelopmentPlanOut


router = APIRouter(
    prefix="/programs/{program_id}/development-plans",
    tags=["Program Development Plans"]
)


@router.get("/", response_model=list[ProgramDevelopmentPlanOut])
def get_development_plans(
    program_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(ProgramDevelopmentPlan)
        .filter(ProgramDevelopmentPlan.program_id == program_id)
        .order_by(ProgramDevelopmentPlan.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramDevelopmentPlanOut)
def add_development_plan(
    program_id: int,
    data: ProgramDevelopmentPlanCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    plan = ProgramDevelopmentPlan(
        program_id=program_id,
        **data.model_dump()
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan


@router.delete("/{plan_id}")
def delete_development_plan(
    program_id: int,
    plan_id: int,
    db: Session = Depends(get_db)
):
    plan = (
        db.query(ProgramDevelopmentPlan)
        .filter(
            ProgramDevelopmentPlan.id == plan_id,
            ProgramDevelopmentPlan.program_id == program_id
        )
        .first()
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Development plan not found"
        )

    db.delete(plan)
    db.commit()

    return {
        "message": "Development plan deleted successfully"
    }
