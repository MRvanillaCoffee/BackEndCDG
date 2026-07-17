from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.instructors import router as instructors_router

app = FastAPI(
    title="Curriculum AI API",
    description="AI Router สำหรับระบบจัดการหลักสูตร",
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(instructors_router)