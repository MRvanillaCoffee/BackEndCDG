from pydantic import BaseModel, Field
from typing import Any, Literal


class AIGenerateRequest(BaseModel):
    target: Literal[
        "course_description",
        "course_objectives",
        "clos",
        "course_topics",
        "teaching_methods",
        "assessment_methods"
    ]

    language: Literal["th", "en", "both"] = "both"

    context: dict[str, Any] = Field(default_factory=dict)

    prompt: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "target": "course_description",
                    "language": "both",
                    "context": {
                        "course_name": "Database Management Systems",
                        "course_code": "CS301",
                        "credits": "3(2-2-5)",
                        "topics": [
                            "Database fundamentals",
                            "Relational database",
                            "SQL",
                            "Database design",
                            "Normalization"
                        ]
                    },
                    "prompt": "Generate a concise formal academic course description."
                }
            ]
        }
    }


class AIGenerateResponse(BaseModel):
    target: str
    result: Any
    model: str