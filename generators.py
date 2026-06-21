# ==========================================
# llm_service.py
# ==========================================

from groq import Groq
from config import GROQ_API_KEY


SYSTEM_PROMPT = """
You are an expert NCF 2023 and NEP 2020 aligned AI Teacher Assistant.

Always:

- Explain like a teacher.
- Use simple language.
- Focus on conceptual understanding.
- Promote competency-based learning.
- Include learning outcomes whenever relevant.
- Include competencies whenever relevant.
- Include activity-based learning.
- Include inclusive teaching strategies.
- Avoid rote learning.
- Encourage critical thinking.
- Use classroom-friendly structure.
"""


# ==========================================
# GROQ CLIENT
# ==========================================

def get_client():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found")

    return Groq(api_key=GROQ_API_KEY)


# ==========================================
# COMMON LLM FUNCTION
# ==========================================

def call_llm(
    prompt: str,
    max_tokens: int = 2000,
    temperature: float = 0.3,
):
    try:
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

        return response.choices[0].message.content

    except Exception as e:
        return f"Generation Error:\n\n{str(e)}"


# ==========================================
# GENERIC GENERATOR
# ==========================================

def generate_content(
    prompt_template: str,
    variables: dict,
    max_tokens: int = 2000
):
    prompt = prompt_template.format(**variables)

    return call_llm(
        prompt=prompt,
        max_tokens=max_tokens
    )
