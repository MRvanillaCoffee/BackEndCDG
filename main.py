import logging
import re

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DataError, IntegrityError
from routes import programs
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    programs,
    program_majors,
    program_careers,
    program_approvals,
    program_instructors,
    program_development_plans,
    program_elo_framework,
    program_ylo,
    program_learning_topics,
    program_schedule,
    program_budget,
    program_course_category,
    program_learning_attributes,
    program_learning_dimension,
    program_plo,
    program_plo_tqf_mapping,
    program_evaluation,
    program_graduation_criteria,
    program_faculty_development,
    program_quality_section,
    quality_kpi,
    program_evaluation_process,
    course,
    program_semester,
    program_course,
    course_instructor,
    plo_course_mapping,
    course_category_assignment,
    program_favorites
)



app = FastAPI(title="Curriculum API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = logging.getLogger("curriculum_api")

# Friendly text for the UNIQUE keys a request can run into (key name as MariaDB reports it).
_DUPLICATE_MESSAGES = {
    "uq_program_course_branch": "This course is already in that semester (same branch).",
    "uq_category_assignment": "This course is already placed in that category.",
    "uq_plo_course_mapping": "This PLO is already mapped to that course.",
    "uq_program_schedule": "A schedule for that semester type already exists for this program.",
    "uq_program_semester": "That year and term already exist for this program.",
    "uq_program_favorite": "This program is already starred by that user.",
    "uq_course_prerequisite": "That prerequisite is already listed for this course.",
    "uq_course_corequisite": "That corequisite is already listed for this course.",
}


def _db_error_code(exc) -> int | None:
    args = getattr(getattr(exc, "orig", None), "args", ())
    return args[0] if args and isinstance(args[0], int) else None


# Safety net for database errors that bad INPUT can cause (a duplicate, a reference to a record that
# does not exist). Routers still validate the common cases themselves for precise messages; this
# catches whatever they miss so the client gets a 409/422 instead of a 500.
# Errors that mean a BUG in our code (e.g. NOT NULL violations) are deliberately NOT disguised:
# they are logged and stay a 500.
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    code = _db_error_code(exc)
    if code == 1062:  # duplicate entry on a UNIQUE key
        key = re.search(r"for key '([^']+)'", str(exc.orig))
        message = _DUPLICATE_MESSAGES.get(key.group(1) if key else "", "This record already exists (duplicate value).")
        return JSONResponse(status_code=409, content={"detail": message})
    if code == 1452:  # foreign key: the referenced record does not exist
        return JSONResponse(status_code=409, content={"detail": "This refers to a record that does not exist."})
    if code == 1451:  # foreign key: the record is still referenced elsewhere
        return JSONResponse(status_code=409, content={"detail": "This record is still in use and cannot be changed or deleted."})
    logger.exception("Unexpected database integrity error (code %s) on %s %s", code, request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.exception_handler(DataError)
async def data_error_handler(request: Request, exc: DataError):
    code = _db_error_code(exc)
    if code in (1264, 1265, 1292, 1366, 1406):  # out of range / too long / wrong value for the column
        logger.warning("Value rejected by the database on %s %s (code %s) — schema validation missed it",
                       request.method, request.url.path, code)
        return JSONResponse(status_code=422, content={"detail": "A value does not fit its database column (too long or out of range)."})
    logger.exception("Unexpected database data error (code %s) on %s %s", code, request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(programs.router)
app.include_router(program_majors.router)
app.include_router(program_careers.router)
app.include_router(program_approvals.router)
app.include_router(program_instructors.router)
app.include_router(program_development_plans.router)
app.include_router(program_elo_framework.router)
app.include_router(program_ylo.router)
app.include_router(program_learning_topics.router)
app.include_router(program_schedule.router)
app.include_router(program_budget.income_router)
app.include_router(program_budget.expense_router)
app.include_router(program_course_category.router)
app.include_router(program_learning_attributes.router)
app.include_router(program_learning_dimension.router)
app.include_router(program_plo.router)
app.include_router(program_plo_tqf_mapping.router)
app.include_router(program_evaluation.router)
app.include_router(program_graduation_criteria.router)
app.include_router(program_faculty_development.router)
app.include_router(program_quality_section.router)
app.include_router(quality_kpi.router)
app.include_router(program_evaluation_process.router)
app.include_router(course.router)
app.include_router(program_semester.router)
app.include_router(program_course.router)
app.include_router(course_instructor.router)
app.include_router(plo_course_mapping.router)
app.include_router(course_category_assignment.router)
app.include_router(program_favorites.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}