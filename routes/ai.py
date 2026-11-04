
import json
import httpx

from fastapi import APIRouter, HTTPException

from ai_schemas import (
    AIGenerateRequest,
    AIGenerateResponse
)

from services.ai_service import generate_content
from services.ollama_service import GEMMA_MODEL

router = APIRouter(
    prefix="/ai",
    tags=["AI Generator"]
)


@router.post(
    "/generate/course-description",
    response_model=AIGenerateResponse
)
async def generate_course_description(
    request: AIGenerateRequest
):
    try:
        if request.target != "course_description":
            raise HTTPException(
                status_code=422,
                detail="This endpoint only supports course_description"
            )

        response = await generate_content(request)

        result = json.loads(response) if isinstance(response, str) else response

        expected_keys = {
            "th": {"th"},
            "en": {"en"},
            "both": {"th", "en"}
        }[request.language]

        if not isinstance(result, dict) or set(result.keys()) != expected_keys:
            raise ValueError("AI returned unexpected JSON fields")

        if not all(
            isinstance(value, str) and value.strip()
            for value in result.values()
        ):
            raise ValueError("AI returned empty or invalid descriptions")

        return {
            "target": request.target,
            "result": result,
            "model": GEMMA_MODEL
        }

    except HTTPException:
        raise

    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(
            status_code=502,
            detail=f"Invalid AI response: {str(e)}"
        )

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Unable to communicate with Ollama"
        )
