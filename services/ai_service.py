from prompts import MAIN_PROMPT, get_prompt
from services.ollama_service import generate_with_ollama


async def generate_content(data):

    task_prompt = get_prompt(data.target)

    if not task_prompt:
        raise ValueError("Unsupported generation target")

    user_context = f"""
COURSE INFORMATION:
{data.context}

LANGUAGE:
{data.language}

ADDITIONAL USER INSTRUCTIONS:
{data.prompt or "No additional instructions."}
"""

    full_prompt = f"""
{MAIN_PROMPT}

{task_prompt}

{user_context}
"""

    result = await generate_with_ollama(full_prompt)

    return result