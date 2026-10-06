
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from database import get_db
from models import Program, ProgramFavorite
from schemas import ProgramCreate, ProgramUpdate, ProgramOut


router = APIRouter(
    prefix="/programs",
    tags=["Programs"]
)

# One relationship per page 1-8 whose presence signals that page has at
# least some content. This is a rough "how far along is this draft"
# heuristic, not a strict completeness check against every field.
_PROGRESS_MILESTONES = [
    lambda p: bool(p.name_th or p.degree_name_th),  # page 1 core identity
    lambda p: bool(p.majors or p.careers_list or p.approvals or p.instructors),  # page 1 lists
    lambda p: bool(p.philosophy or p.objectives or p.ylos or p.development_plans),  # page 2
    lambda p: bool(p.learning_topics or p.schedules or p.budget_incomes or p.course_categories),  # page 3
    lambda p: bool(p.learning_attributes or p.plos or p.plo_tqf_mappings),  # page 4
    lambda p: bool(p.evaluation is not None or p.graduation_criteria),  # page 5
    lambda p: bool(p.faculty_development),  # page 6
    lambda p: bool(p.quality_sections or p.quality_kpis),  # page 7
    lambda p: bool(p.evaluation_processes),  # page 8
]


def _compute_progress(program: Program) -> int:
    done = sum(1 for check in _PROGRESS_MILESTONES if check(program))
    return round(done / len(_PROGRESS_MILESTONES) * 100)


def _eager_load(query):
    # Avoids N+1 queries when computing progress across a list of programs —
    # one extra query per relationship instead of one per relationship per row.
    return query.options(
        selectinload(Program.majors),
        selectinload(Program.careers_list),
        selectinload(Program.approvals),
        selectinload(Program.instructors),
        selectinload(Program.development_plans),
        selectinload(Program.ylos),
        selectinload(Program.learning_topics),
        selectinload(Program.schedules),
        selectinload(Program.budget_incomes),
        selectinload(Program.course_categories),
        selectinload(Program.learning_attributes),
        selectinload(Program.plos),
        selectinload(Program.plo_tqf_mappings),
        selectinload(Program.evaluation),
        selectinload(Program.graduation_criteria),
        selectinload(Program.faculty_development),
        selectinload(Program.quality_sections),
        selectinload(Program.quality_kpis),
        selectinload(Program.evaluation_processes),
        selectinload(Program.favorites)
    )


def _to_out(program: Program, starred_ids: set[int]) -> ProgramOut:
    out = ProgramOut.model_validate(program)
    out.progress = _compute_progress(program)
    out.is_starred = program.id in starred_ids
    return out


# ============================================================
# GET ALL PROGRAMS
# ============================================================

@router.get(
    "/",
    response_model=list[ProgramOut]
)
def get_programs(
    user_id: int | None = Query(None, description="If given, flags is_starred and enables starred_only"),
    starred_only: bool = Query(False, description="Only return programs starred by user_id"),
    db: Session = Depends(get_db)
):
    query = _eager_load(db.query(Program)).order_by(Program.id.desc())

    starred_ids: set[int] = set()
    if user_id is not None:
        starred_ids = {
            f.program_id for f in
            db.query(ProgramFavorite).filter(ProgramFavorite.user_id == user_id).all()
        }
        if starred_only:
            if not starred_ids:
                return []
            query = query.filter(Program.id.in_(starred_ids))

    programs = query.all()
    return [_to_out(p, starred_ids) for p in programs]


# ============================================================
# GET ONE PROGRAM
# ============================================================

@router.get(
    "/{program_id}",
    response_model=ProgramOut
)
def get_program(
    program_id: int,
    user_id: int | None = Query(None, description="If given, flags is_starred for this program"),
    db: Session = Depends(get_db)
):
    program = (
        _eager_load(db.query(Program))
        .filter(Program.id == program_id)
        .first()
    )

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    starred_ids: set[int] = set()
    if user_id is not None:
        exists = (
            db.query(ProgramFavorite)
            .filter(ProgramFavorite.program_id == program_id, ProgramFavorite.user_id == user_id)
            .first()
        )
        if exists:
            starred_ids = {program_id}

    return _to_out(program, starred_ids)


# ============================================================
# CREATE PROGRAM
# ============================================================

@router.post(
    "/",
    response_model=ProgramOut
)
def create_program(
    data: ProgramCreate,
    db: Session = Depends(get_db)
):
    program = Program(
        **data.model_dump()
    )

    db.add(program)
    db.commit()
    db.refresh(program)

    return _to_out(program, set())


# ============================================================
# UPDATE PROGRAM
# ============================================================

@router.put(
    "/{program_id}",
    response_model=ProgramOut
)
def update_program(
    program_id: int,
    data: ProgramUpdate,
    db: Session = Depends(get_db)
):
    program = (
        db.query(Program)
        .filter(Program.id == program_id)
        .first()
    )

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(program, field, value)

    db.commit()
    db.refresh(program)

    return _to_out(program, set())


# ============================================================
# DELETE PROGRAM
# ============================================================

@router.delete(
    "/{program_id}"
)
def delete_program(
    program_id: int,
    db: Session = Depends(get_db)
):
    program = (
        db.query(Program)
        .filter(Program.id == program_id)
        .first()
    )

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program not found"
        )

    db.delete(program)
    db.commit()

    return {
        "message": "Program deleted successfully",
        "program_id": program_id
    }
