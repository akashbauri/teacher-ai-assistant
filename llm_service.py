from groq import Groq
from config import GROQ_API_KEY


SYSTEM_PROMPT = """
You are an expert NCF 2023 and NEP 2020 aligned AI Teacher Assistant.
Explain like a teacher.
Use simple language.
Promote competency-based learning.
Use activity-based learning.
Include learning outcomes and competencies whenever relevant.
"""


def get_client():

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found"
        )

    return Groq(
        api_key=GROQ_API_KEY
    )


def call_llm(
    prompt,
    max_tokens=2000,
    temperature=0.3
):

    client = get_client()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return (
        response
        .choices[0]
        .message
        .content
    )
