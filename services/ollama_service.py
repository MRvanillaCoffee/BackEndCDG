import os
import httpx

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

GEMMA_MODEL = os.getenv(
    "GEMMA_MODEL",
    "gemma3:4b"
)


async def generate_with_ollama(prompt: str):

    url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/chat"

    payload = {
        "model": GEMMA_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.3,
            "num_ctx": 4096
        }
    }

    timeout = httpx.Timeout(
        connect=10.0,
        read=300.0,
        write=30.0,
        pool=10.0
    )

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()

    data = response.json()

    if "message" not in data or "content" not in data["message"]:
        raise RuntimeError("Invalid response received from Ollama")

    return data["message"]["content"]