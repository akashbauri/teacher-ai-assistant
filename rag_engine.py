import traceback

from groq import Groq

from config import (
    GROQ_API_KEY
)

from chroma_manager import (
    get_context
)

from utils import (
    search_web,
    format_web_results
)


# ==========================================
# GROQ CLIENT
# ==========================================

def get_client():

    if not GROQ_API_KEY:

        raise Exception(
            "GROQ_API_KEY not found."
        )

    return Groq(
        api_key=GROQ_API_KEY
    )


# ==========================================
# COMMON LLM FUNCTION
# ==========================================

def call_llm(
    prompt,
    max_tokens=1500
):

    try:

        client = get_client()

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=max_tokens
        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        return (
            f"Generation Error:\n\n{str(e)}"
        )


# ==========================================
# EDUCATIONAL FORMATTER
# ==========================================

def build_education_prompt(
    topic,
    context,
    student_level
):

    return f"""
You are an expert teacher.

Student Level:
{student_level}

DOCUMENT:

{context}

QUESTION:

{topic}

Provide answer in this format:

# Explanation

Explain simply.

# Key Concepts

Bullet points.

# Flow Chart

Use arrows.

Example:

Concept
↓
Step 1
↓
Step 2

# Mind Map

Concept
├── Idea 1
├── Idea 2
└── Idea 3

# Exam Tips

Important points.

# Summary

Short summary.
"""


# ==========================================
# QUESTION ANSWERING
# ==========================================

def rag_answer(
    question,
    student_level="Class 5"
):

    try:

        context = get_context(
            question,
            top_k=5
        )

        if context.strip():

            prompt = build_education_prompt(
                question,
                context,
                student_level
            )

            answer = call_llm(
                prompt,
                1200
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

        prompt = build_education_prompt(
            question,
            web_context,
            student_level
        )

        answer = call_llm(
            prompt,
            1200
        )

        return {
            "answer": answer,
            "source": "Web Search"
        }

    except Exception:

        return {
            "answer":
                traceback.format_exc(),
            "source":
                "Error"
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

        return (
            "No relevant content found "
            "in uploaded document."
        )

    prompt = f"""
Create detailed notes.

TOPIC:
{topic}

DOCUMENT:
{context}

Student Level:
{student_level}

Include:

# Introduction

# Key Concepts

# Important Points

# Flow Chart

# Mind Map

# Exam Tips

# Summary
"""

    return call_llm(
        prompt,
        1500
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

        return (
            "No relevant content found "
            "in uploaded document."
        )

    prompt = f"""
Generate 20 MCQs.

TOPIC:
{topic}

DOCUMENT:
{context}

Difficulty:
{difficulty}

For every question:

Q1

A)
B)
C)
D)

Correct Answer:

Explanation:
"""

    return call_llm(
        prompt,
        1800
    )


# ==========================================
# QUESTION PAPER
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

        return (
            "No relevant content found "
            "in uploaded document."
        )

    prompt = f"""
Create a complete question paper.

TOPIC:
{topic}

DOCUMENT:
{context}

MARKS:
{marks}

DIFFICULTY:
{difficulty}

Include:

SECTION A

Very Short Questions

SECTION B

Short Questions

SECTION C

Long Questions

Provide marks distribution.
"""

    return call_llm(
        prompt,
        1800
    )
