import streamlit as st
from openai import OpenAI


def get_client():
    api_key = st.secrets["OPENROUTER_API_KEY"]

    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )


def rag_answer(question, student_level="Class 5"):
    return {
        "answer": f"Test Answer: {question}",
        "source": "Test Source"
    }


def generate_document_notes(
    topic,
    student_level="Class 5"
):
    return f"Notes Generated For: {topic}"


def generate_document_mcqs(
    topic,
    difficulty="Easy"
):
    return f"MCQs Generated For: {topic}"


def generate_document_question_paper(
    topic,
    marks=20,
    difficulty="Mixed"
):
    return f"Question Paper Generated For: {topic}"
