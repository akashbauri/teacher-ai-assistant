import streamlit as st
from openai import OpenAI


def get_client():
    return OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )


def rag_answer(question, student_level="Class 5"):

    client = get_client()

    prompt = f"""
Answer the following question for a {student_level} student.

Question:
{question}

Give a detailed answer.
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
        max_tokens=1500
    )

    return {
        "answer": response.choices[0].message.content,
        "source": "AI Generated"
    }


def generate_document_notes(
    topic,
    student_level="Class 5"
):

    client = get_client()

    prompt = f"""
Create detailed study notes.

Topic:
{topic}

Student Level:
{student_level}

Include:
1. Introduction
2. Key Concepts
3. Important Points
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


def generate_document_mcqs(
    topic,
    difficulty="Easy"
):

    client = get_client()

    prompt = f"""
Generate 10 multiple-choice questions.

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

Generate 10 MCQs with answers.
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


def generate_document_question_paper(
    topic,
    marks=20,
    difficulty="Mixed"
):

    client = get_client()

    prompt = f"""
Create a complete question paper.

Topic:
{topic}

Total Marks:
{marks}

Difficulty:
{difficulty}

Include:
- Very Short Questions
- Short Questions
- Long Questions
- Marks Distribution
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
