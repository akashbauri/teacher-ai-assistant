import streamlit as st
from openai import OpenAI

from chroma_manager import get_context
from utils import search_web, format_web_results


def get_client():

    return OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )


def call_llm(
    prompt,
    max_tokens=3000
):

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
        max_tokens=max_tokens
    )

    return response.choices[0].message.content


def rag_answer(
    question,
    student_level="Class 5"
):

    context = get_context(
        question,
        top_k=5
    )

    if context.strip():

        prompt = f"""
You are an expert teacher.

Use the uploaded document first.

DOCUMENT:

{context}

QUESTION:

{question}

Student Level:
{student_level}

Give a detailed answer.
"""

        answer = call_llm(
            prompt,
            2000
        )

        return {
            "answer": answer,
            "source": "FAISS Document Search"
        }

    web_results = search_web(
        question
    )

    web_context = format_web_results(
        web_results
    )

    prompt = f"""
Answer the question using web search results.

WEB RESULTS:

{web_context}

QUESTION:

{question}

Student Level:
{student_level}
"""

    answer = call_llm(
        prompt,
        2000
    )

    return {
        "answer": answer,
        "source": "Web Search"
    }


def generate_document_notes(
    topic,
    student_level="Class 5"
):

    context = get_context(
        topic,
        top_k=5
    )

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

    return call_llm(
        prompt,
        3000
    )


def generate_document_mcqs(
    topic,
    difficulty="Mixed"
):

    context = get_context(
        topic,
        top_k=5
    )

    prompt = f"""
Generate 10 MCQs ONLY from the uploaded document.

DOCUMENT:

{context}

TOPIC:
{topic}

Difficulty:
{difficulty}

For every question provide:

Question
A)
B)
C)
D)

Correct Answer

Explanation
"""

    return call_llm(
        prompt,
        3500
    )


def generate_document_question_paper(
    topic,
    marks=20,
    difficulty="Mixed"
):

    context = get_context(
        topic,
        top_k=5
    )

    prompt = f"""
Create a complete question paper.

DOCUMENT:

{context}

TOPIC:
{topic}

TOTAL MARKS:
{marks}

DIFFICULTY:
{difficulty}

Include:

Section A:
Very Short Questions

Section B:
Short Questions

Section C:
Long Questions

Provide marks distribution.
"""

    return call_llm(
        prompt,
        3500
    )
