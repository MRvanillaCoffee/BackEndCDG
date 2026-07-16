import json
import os
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
GEMMA_MODEL = os.getenv("GEMMA_MODEL", "gemma3:4b")


class ChatRequest(BaseModel):
    prompt: str


@app.get("/")
def read_root() -> dict[str, Any]:
    return {"message": "FastAPI is running with Ollama and Gemma"}


