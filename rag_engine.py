import streamlit as st
from openai import OpenAI

from chroma_manager import get_context
from utils import search_web, format_web_results


# ==========================================
# OPENROUTER CLIENT
# ==========================================

def get_client():

    return OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )


# ==========================================
# COMMON LLM FUNCTION
# ==========================================

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


# ==========================================
# QUESTION ANSWERING
# ==========================================

def rag_answer(
    question,
    student_level="Class 5"
):

    context = get_context(
        question,
        top_k=5
    )

    # Use uploaded document first

    if context and context.strip():

        prompt = f"""
You are an expert teacher.

Use ONLY the uploaded document.

DOCUMENT:

{context}

QUESTION:

{question}

Student Level:
{student_level}

Instructions:

- Answer clearly
- Explain concepts simply
- Give examples if available
- Do not invent facts outside the document
"""

        answer = call_llm(
            prompt,
            2000
        )

        return {
            "answer": answer,
            "source": "FAISS Document Search"
        }

    # Fallback to Web Search

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

Give a detailed answer.
"""

    answer = call_llm(
        prompt,
        2000
    )

    return {
        "answer": answer,
        "source": "Web Search"
    }


# ==========================================
# NOTES GENERATOR
# ==========================================

def generate_document_notes(
    topic,
    student_level="Class 5"
):

    context = get_context(
        topic,
        top_k=5
    )

    if not context.strip():

        return """
No relevant content found in the uploaded document.

Please upload a document containing this topic.
"""

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
4. Examples
5. Summary
6. Exam Tips

Use simple language.
"""

    return call_llm(
        prompt,
        3000
    )


# ==========================================
# MCQ GENERATOR
# ==========================================

def generate_document_mcqs(
    topic,
    difficulty="Mixed"
):

    context = get_context(
        topic,
        top_k=5
    )

    if not context.strip():

        return """
No relevant content found in the uploaded document.

Please upload a document containing this topic.
"""

    prompt = f"""
Generate 10 high-quality MCQs ONLY from the uploaded document.

DOCUMENT:

{context}

TOPIC:
{topic}

Difficulty:
{difficulty}

Requirements:

- 4 options
- One correct answer
- Explanation
- Mix of Easy, Medium and Hard
- Exam style questions

Format:

Q1.
A)
B)
C)
D)

Correct Answer:

Explanation:
"""

    return call_llm(
        prompt,
        3500
    )


# ==========================================
# QUESTION PAPER GENERATOR
# ==========================================

def generate_document_question_paper(
    topic,
    marks=20,
    difficulty="Mixed"
):

    context = get_context(
        topic,
        top_k=5
    )

    if not context.strip():

        return """
No relevant content found in the uploaded document.

Please upload a document containing this topic.
"""

    prompt = f"""
Create a complete question paper ONLY from the uploaded document.

DOCUMENT:

{context}

TOPIC:
{topic}

TOTAL MARKS:
{marks}

DIFFICULTY:
{difficulty}

Structure:

SECTION A
Very Short Questions

SECTION B
Short Questions

SECTION C
Long Questions

Requirements:

- Proper marks distribution
- Balanced difficulty
- Exam format
- Clear instructions
"""

    return call_llm(
        prompt,
        3500
    )
