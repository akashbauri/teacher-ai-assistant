import streamlit as st
from openai import OpenAI

def get_client():
api_key = st.secrets["OPENROUTER_API_KEY"]

```
return OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)
```

def rag_answer(question, student_level="Class 5"):

```
client = get_client()

response = client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[
        {
            "role": "user",
            "content": f"Explain for {student_level} student: {question}"
        }
    ]
)

return {
    "answer": response.choices[0].message.content,
    "source": "AI Generated"
}
```

def generate_document_notes(topic, student_level="Class 5"):

```
client = get_client()

response = client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[
        {
            "role": "user",
            "content": f"Create notes about {topic} for {student_level} students."
        }
    ]
)

return response.choices[0].message.content
```

def generate_document_mcqs(topic, difficulty="Easy"):

```
client = get_client()

response = client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[
        {
            "role": "user",
            "content": f"Generate 10 MCQs about {topic} with {difficulty} difficulty."
        }
    ]
)

return response.choices[0].message.content
```

def generate_document_question_paper(
topic,
marks=20,
difficulty="Mixed"
):

```
client = get_client()

response = client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[
        {
            "role": "user",
            "content": f"Create a {marks} marks question paper on {topic} with {difficulty} difficulty."
        }
    ]
)

return response.choices[0].message.content
```
