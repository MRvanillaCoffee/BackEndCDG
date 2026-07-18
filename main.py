from fastapi import FastAPI
from routes import programs
from fastapi.middleware.cors import CORSMiddleware
from routes import programs, auth, users



app = FastAPI(title="Curriculum API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(programs.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}