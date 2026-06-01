import streamlit as st
from openai import OpenAI

from chroma_manager import get_context
from utils import search_web, format_web_results


def get_client():
    return OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )


def answer_from_document(question, student_level="Class 5"):
    context = get_context(question)

    if not context:
        return None

    prompt = f"""
You are an AI Teacher Assistant.

Explain like a {student_level} student.

DOCUMENT:
{context}

QUESTION:
{question}

ANSWER:
"""

    client = get_client()

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

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "source": "Uploaded Document"
    }


def answer_from_web(question, student_level="Class 5"):
    results = search_web(question)

    web_content = format_web_results(results)

    prompt = f"""
You are an AI Teacher Assistant.

Explain like a {student_level} student.

WEB CONTENT:
{web_content}

QUESTION:
{question}

ANSWER:
"""

    client = get_client()

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

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "source": "Web Search"
    }


def rag_answer(question, student_level="Class 5"):
    document_result = answer_from_document(
        question,
        student_level
    )

    if document_result:
        return document_result

    return answer_from_web(
        question,
        student_level
    )


def generate_document_notes(topic, student_level="Class 5"):
    context = get_context(topic)

    return f"""
# Notes

Topic: {topic}

Student Level: {student_level}

{context}
"""


def generate_document_mcqs(topic, difficulty="Mixed"):
    context = get_context(topic)

    return f"""
Generate MCQs from:

Topic: {topic}

Difficulty: {difficulty}

Content:

{context}
"""


def generate_document_question_paper(
    topic,
    marks=20,
    difficulty="Mixed"
):
    context = get_context(topic)

    return f"""
Generate Question Paper

Topic: {topic}

Marks: {marks}

Difficulty: {difficulty}

Content:

{context}
"""
