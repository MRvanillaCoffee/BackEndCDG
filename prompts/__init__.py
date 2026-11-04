from prompts.main_prompt import MAIN_PROMPT

from prompts.tasks.course_description import COURSE_DESCRIPTION_PROMPT

TASK_PROMPTS = {
    "course_description": COURSE_DESCRIPTION_PROMPT,
}


def get_prompt(target: str):
    return TASK_PROMPTS.get(target)