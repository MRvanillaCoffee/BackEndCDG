COURSE_DESCRIPTION_PROMPT = """
TASK: Generate a formal course description.

REQUIREMENTS:
1. Describe the scope and main content of the course.
2. Summarize the important knowledge and skills.
3. Keep the description concise and coherent.
4. Do not simply list the course topics.
5. Do not invent course content.

OUTPUT FORMAT:
{
    "th": "Thai course description",
    "en": "English course description"
}
"""