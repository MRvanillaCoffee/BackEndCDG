from fastapi import FastAPI
from routes import programs
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    programs,
    program_majors,
    program_careers,
    program_approvals,
    program_instructors,
    program_development_plans,
    program_elo_framework
)



app = FastAPI(title="Curriculum API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(programs.router)
app.include_router(program_majors.router)
app.include_router(program_careers.router)
app.include_router(program_approvals.router)
app.include_router(program_instructors.router)
app.include_router(program_development_plans.router)
app.include_router(program_elo_framework.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}