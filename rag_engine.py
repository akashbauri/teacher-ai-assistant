import streamlit as st
from openai import OpenAI


def get_client():

    if "OPENROUTER_API_KEY" not in st.secrets:
        raise Exception(
            "OPENROUTER_API_KEY not found in Streamlit Secrets"
        )

    return OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )


def call_llm(prompt, max_tokens=2500):

    client = get_client()

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content


def rag_answer(
    question,
    student_level="Class 5"
):

    prompt = f"""
Answer the following question.

Student Level:
{student_level}

Question:
{question}

Give a detailed answer in simple language.
"""

    answer = call_llm(prompt, 1500)

    return {
        "answer": answer,
        "source": "OpenRouter AI"
    }


def generate_document_notes(
    topic,
    student_level="Class 5"
):

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

5. Exam Tips
"""

    return call_llm(prompt, 2500)


def generate_document_mcqs(
    topic,
    difficulty="Easy"
):

    prompt = f"""
Generate 10 MCQs.

Topic:
{topic}

Difficulty:
{difficulty}

Format:

Q1.

A)

B)

C)

D)

Answer:

Generate all 10 questions with answers.
"""

    return call_llm(prompt, 3000)


def generate_document_question_paper(
    topic,
    marks=20,
    difficulty="Mixed"
):

    prompt = f"""
Create a complete question paper.

Topic:
{topic}

Total Marks:
{marks}

Difficulty:
{difficulty}

Include:

Section A:
Very Short Questions

Section B:
Short Questions

Section C:
Long Questions

Also provide marks distribution.
"""

    return call_llm(prompt, 3500)
