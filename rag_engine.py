import streamlit as st
from openai import OpenAI

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

# QUESTION ANSWERING

# ==========================================

def rag_answer(
question,
student_level="Class 5"
):

```
try:

    client = get_client()

    prompt = f"""
```

Answer the question for a {student_level} student.

Question:
{question}

Use simple language.
"""

```
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1500
    )

    return {
        "answer": response.choices[0].message.content,
        "source": "AI Generated"
    }

except Exception as e:

    return {
        "answer": f"Error: {str(e)}",
        "source": "Error"
    }
```

# ==========================================

# NOTES

# ==========================================

def generate_document_notes(
topic,
student_level="Class 5"
):

```
client = get_client()

prompt = f"""
```

Create detailed study notes.

Topic:
{topic}

Student Level:
{student_level}

Include:

1. Introduction
2. Important Concepts
3. Key Points
4. Summary
   """

   response = client.chat.completions.create(
   model="deepseek/deepseek-chat",
   messages=[
   {
   "role": "user",
   "content": prompt
   }
   ],
   temperature=0.4,
   max_tokens=2500
   )

   return response.choices[0].message.content

# ==========================================

# MCQ GENERATOR

# ==========================================

def generate_document_mcqs(
topic,
difficulty="Easy"
):

```
client = get_client()

prompt = f"""
```

Generate 10 MCQs with answers.

Topic:
{topic}

Difficulty:
{difficulty}

Format:

Q1.
A.
B.
C.
D.

Answer:
"""

```
response = client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.4,
    max_tokens=3000
)

return response.choices[0].message.content
```

# ==========================================

# QUESTION PAPER

# ==========================================

def generate_document_question_paper(
topic,
marks=20,
difficulty="Mixed"
):

```
client = get_client()

prompt = f"""
```

Create a question paper.

Topic:
{topic}

Total Marks:
{marks}

Difficulty:
{difficulty}

Include:

* Very Short Questions
* Short Questions
* Long Questions
* Marks Distribution
  """

  response = client.chat.completions.create(
  model="deepseek/deepseek-chat",
  messages=[
  {
  "role": "user",
  "content": prompt
  }
  ],
  temperature=0.4,
  max_tokens=3500
  )

  return response.choices[0].message.content
