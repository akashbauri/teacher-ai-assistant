```python
import streamlit as st
from openai import OpenAI

from chroma_manager import get_context
from utils import (
    search_web,
    format_web_results
)

# ==========================================
# OPENROUTER CLIENT
# ==========================================

def get_client():

    return OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )

# ==========================================
# DOCUMENT QA
# ==========================================

def answer_from_document(
    question,
    student_level="Class 5"
):

    context = get_context(
        question
    )

    if not context.strip():

        return {
            "answer": "",
            "source": "No Document Source Found"
        }

    prompt = f"""
You are an AI Teacher Assistant.

IMPORTANT:

Explain like a {student_level} student.

Use simple language.

Use only the provided document context.

DOCUMENT CONTEXT:

{context}

QUESTION:

{question}

ANSWER:
"""

    client = get_client()

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=2000
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "source": "Uploaded Document"
    }

# ==========================================
# WEB FALLBACK
# ==========================================

def answer_from_web(
    question,
    student_level="Class 5"
):

    web_results = search_web(
        question
    )

    web_content = format_web_results(
        web_results
    )

    prompt = f"""
You are an AI Teacher Assistant.

Explain for:

{student_level}

Use simple language.

WEB CONTENT:

{web_content}

QUESTION:

{question}

ANSWER:
"""

    client = get_client()

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=2000
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "source": "Web Search"
    }

# ==========================================
# HYBRID RAG
# ==========================================

def rag_answer(
    question,
    student_level="Class 5"
):

    document_result = answer_from_document(
        question,
        student_level
    )

    if document_result["answer"]:

        return document_result

    web_result = answer_from_web(
        question,
        student_level
    )

    return web_result

# ==========================================
# GENERATE NOTES FROM DOCUMENT
# ==========================================

def generate_document_notes(
    topic,
    student_level="Class 5"
):

    context = get_context(
        topic
    )

    prompt = f"""
Create study notes.

Student Level:
{student_level}

DOCUMENT:

{context}

TOPIC:

{topic}

Create:

- Important Points
- Summary
- Key Facts
"""

    client = get_client()

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3",
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

# ==========================================
# GENERATE MCQS FROM DOCUMENT
# ==========================================

def generate_document_mcqs(
    topic,
    difficulty="Mixed"
):

    context = get_context(
        topic
    )

    prompt = f"""
Generate MCQs.

Difficulty:
{difficulty}

DOCUMENT:

{context}

TOPIC:

{topic}

Provide:

Question
4 Options
Correct Answer
"""

    client = get_client()

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3",
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

# ==========================================
# GENERATE QUESTION PAPER
# ==========================================

def generate_document_question_paper(
    topic,
    marks=20,
    difficulty="Mixed"
):

    context = get_context(
        topic
    )

    prompt = f"""
Generate a Question Paper.

Marks:
{marks}

Difficulty:
{difficulty}

DOCUMENT:

{context}

TOPIC:

{topic}

Create a proper exam paper.
"""

    client = get_client()

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=4000
    )

    return response.choices[0].message.content
```
