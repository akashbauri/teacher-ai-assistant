import streamlit as st
from openai import OpenAI

from chroma_manager import get_context


def get_client():

    return OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )


def rag_answer(
    question,
    student_level="Class 5"
):

    context = get_context(
        question,
        top_k=5
    )

    client = get_client()

    prompt = f"""
You are an expert teacher.

Use ONLY the uploaded document.

DOCUMENT:

{context}

QUESTION:

{question}

Student Level:
{student_level}

Answer in simple language.
"""

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=2000
    )

    return {
        "answer": response.choices[0].message.content,
        "source": "Uploaded Document"
    }


def generate_document_notes(
    topic,
    student_level="Class 5"
):

    context = get_context(
        topic,
        top_k=5
    )

    client = get_client()

    prompt = f"""
Create detailed study notes.

DOCUMENT:

{context}

TOPIC:
{topic}

Student Level:
{student_level}

Include:

1. Introduction
2. Important Concepts
3. Key Points
4. Summary
5. Exam Tips
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
        max_tokens=3000
    )

    return response.choices[0].message.content


def generate_document_mcqs(
    topic,
    difficulty="Mixed"
):

    context = get_context(
        topic,
        top_k=5
    )

    client = get_client()

    prompt = f"""
Generate 10 MCQs ONLY from the document.

DOCUMENT:

{context}

TOPIC:
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
Explanation:
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


def generate_document_question_paper(
    topic,
    marks=20,
    difficulty="Mixed"
):

    context = get_context(
        topic,
        top_k=5
    )

    client = get_client()

    prompt = f"""
Create a question paper ONLY from the document.

DOCUMENT:

{context}

TOPIC:
{topic}

Marks:
{marks}

Difficulty:
{difficulty}

Include:

1. Very Short Questions
2. Short Questions
3. Long Questions
4. Marks Distribution
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
