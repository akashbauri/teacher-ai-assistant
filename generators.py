import streamlit as st
from openai import OpenAI

from prompts import (
DEFAULT_SYSTEM_PROMPT,
EXPLAIN_TOPIC_PROMPT,
NOTES_PROMPT,
MCQ_PROMPT,
QUESTION_PAPER_PROMPT,
LESSON_PLAN_PROMPT,
TEACHING_GUIDE_PROMPT,
HOMEWORK_PROMPT,
WORKSHEET_PROMPT,
BLOOM_PROMPT
)

# ==========================================

# OPENROUTER CLIENT

# ==========================================

def get_client():

```
if "OPENROUTER_API_KEY" not in st.secrets:
    raise Exception(
        "OPENROUTER_API_KEY not found in Streamlit Secrets"
    )

api_key = st.secrets["OPENROUTER_API_KEY"]

if not api_key:
    raise Exception(
        "OPENROUTER_API_KEY is empty"
    )

return OpenAI(
    api_key=api_key.strip(),
    base_url="https://openrouter.ai/api/v1"
)
```

# ==========================================

# MAIN LLM FUNCTION

# ==========================================

def call_llm(user_prompt):

```
client = get_client()

try:

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": DEFAULT_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.4,
        max_tokens=3000
    )

    return response.choices[0].message.content

except Exception as e:

    return f"LLM Error: {str(e)}"
```

# ==========================================

# EXPLAIN TOPIC

# ==========================================

def explain_topic(
topic,
student_level="Class 5",
teaching_style="Beginner Friendly"
):

```
prompt = EXPLAIN_TOPIC_PROMPT.format(
    topic=topic,
    student_level=student_level,
    teaching_style=teaching_style
)

return call_llm(prompt)
```

# ==========================================

# NOTES

# ==========================================

def generate_notes(
content,
student_level="Class 5"
):

```
prompt = NOTES_PROMPT.format(
    content=content,
    student_level=student_level
)

return call_llm(prompt)
```

# ==========================================

# MCQS

# ==========================================

def generate_mcqs(
content,
difficulty="Easy"
):

```
prompt = MCQ_PROMPT.format(
    content=content,
    difficulty=difficulty
)

return call_llm(prompt)
```

# ==========================================

# QUESTION PAPER

# ==========================================

def generate_question_paper(
content,
marks=20,
difficulty="Mixed",
student_level="Class 5"
):

```
prompt = QUESTION_PAPER_PROMPT.format(
    content=content,
    marks=marks,
    difficulty=difficulty,
    student_level=student_level
)

return call_llm(prompt)
```

# ==========================================

# LESSON PLAN

# ==========================================

def generate_lesson_plan(
topic,
student_level="Class 5"
):

```
prompt = LESSON_PLAN_PROMPT.format(
    topic=topic,
    student_level=student_level
)

return call_llm(prompt)
```

# ==========================================

# TEACHING GUIDE

# ==========================================

def generate_teaching_guide(
topic,
student_level="Class 5",
teaching_style="Beginner Friendly"
):

```
prompt = TEACHING_GUIDE_PROMPT.format(
    topic=topic,
    student_level=student_level,
    teaching_style=teaching_style
)

return call_llm(prompt)
```

# ==========================================

# HOMEWORK

# ==========================================

def generate_homework(
topic,
student_level="Class 5"
):

```
prompt = HOMEWORK_PROMPT.format(
    topic=topic,
    student_level=student_level
)

return call_llm(prompt)
```

# ==========================================

# WORKSHEET

# ==========================================

def generate_worksheet(
content,
student_level="Class 5"
):

```
prompt = WORKSHEET_PROMPT.format(
    content=content,
    student_level=student_level
)

return call_llm(prompt)
```

# ==========================================

# BLOOM QUESTIONS

# ==========================================

def generate_bloom_questions(
topic,
student_level="Class 5"
):

```
prompt = BLOOM_PROMPT.format(
    topic=topic,
    student_level=student_level
)

return call_llm(prompt)
```

# ==========================================

# ROUTER

# ==========================================

def generate_from_action(
action,
content,
student_level,
teaching_style
):

```
action = action.lower()

if action == "explain":
    return explain_topic(
        content,
        student_level,
        teaching_style
    )

elif action == "notes":
    return generate_notes(
        content,
        student_level
    )

elif action == "mcqs":
    return generate_mcqs(
        content,
        "Mixed"
    )

elif action == "question paper":
    return generate_question_paper(
        content,
        20,
        "Mixed",
        student_level
    )

elif action == "lesson plan":
    return generate_lesson_plan(
        content,
        student_level
    )

elif action == "teaching guide":
    return generate_teaching_guide(
        content,
        student_level,
        teaching_style
    )

elif action == "homework":
    return generate_homework(
        content,
        student_level
    )

elif action == "worksheet":
    return generate_worksheet(
        content,
        student_level
    )

elif action == "bloom":
    return generate_bloom_questions(
        content,
        student_level
    )

return explain_topic(
    content,
    student_level,
    teaching_style
)
```
