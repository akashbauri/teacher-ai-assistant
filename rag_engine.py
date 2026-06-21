# generators.py

import traceback
from groq import Groq

from config import GROQ_API_KEY
from chroma_manager import get_context
from utils import search_web, format_web_results


# =====================================================
# GROQ CLIENT
# =====================================================

def get_client():
    """
    Initialize Groq client.
    """

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found.")

    return Groq(api_key=GROQ_API_KEY)


# =====================================================
# LLM CALL
# =====================================================

SYSTEM_PROMPT = """
You are an expert NCF 2023 and NEP 2020 aligned AI Teacher Assistant.

Always:

- Explain like a teacher
- Use simple language
- Focus on conceptual understanding
- Promote competency-based learning
- Include learning outcomes
- Include competencies
- Include activity-based learning
- Include inclusive teaching strategies
- Avoid rote memorization
- Encourage critical thinking
- Use real-life examples
- Explain in classroom-friendly language
"""


def call_llm(prompt: str, max_tokens: int = 2000) -> str:
    """
    Send prompt to Groq LLM.
    """

    try:
        client = get_client()

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Generation Error:\n\n{str(e)}"


# =====================================================
# EDUCATION PROMPT BUILDER
# =====================================================

def build_education_prompt(
    topic: str,
    context: str,
    student_level: str
) -> str:

    return f"""
Create a complete NCF 2023 aligned explanation.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

REFERENCE CONTENT:
{context}

Generate:

# Simple Explanation

Explain like a teacher.

# Learning Outcomes

# Competencies

# Key Concepts

# Real Life Examples

# Activity Based Learning

# Inclusive Teaching Strategy

# Flow Chart

Use arrows.

# Mind Map

Use tree structure.

# Assessment Questions

Easy Questions

Moderate Questions

Hard Questions

# Exam Tips

# Summary

Use simple language.
"""


# =====================================================
# RAG QUESTION ANSWERING
# =====================================================

def rag_answer(
    question: str,
    student_level: str = "Class 5"
) -> dict:

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
                max_tokens=1800
            )

            return {
                "answer": answer,
                "source": "Document Knowledge Base"
            }

        web_results = search_web(question)

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
            max_tokens=1800
        )

        return {
            "answer": answer,
            "source": "Web Search"
        }

    except Exception:

        return {
            "answer": traceback.format_exc(),
            "source": "Error"
        }


# =====================================================
# NOTES GENERATOR
# =====================================================

def generate_document_notes(
    topic: str,
    student_level: str = "Class 5"
) -> str:

    context = get_context(
        topic,
        top_k=5
    )

    if not context.strip():
        return "No relevant content found in uploaded document."

    prompt = f"""
Generate NCF 2023 aligned study notes.

TOPIC:
{topic}

DOCUMENT:
{context}

STUDENT LEVEL:
{student_level}

Generate:

# Chapter Overview

# Learning Outcomes

# Competencies

# Key Concepts

# Detailed Notes

# Real Life Examples

# Activity Based Learning

# Inclusive Teaching Strategy

# Flow Chart

# Mind Map

# Revision Notes

# Summary
"""

    return call_llm(
        prompt,
        max_tokens=2200
    )


# =====================================================
# MCQ GENERATOR
# =====================================================

def generate_document_mcqs(
    topic: str,
    difficulty: str = "Mixed"
) -> str:

    context = get_context(
        topic,
        top_k=5
    )

    if not context.strip():
        return "No relevant content found in uploaded document."

    prompt = f"""
Generate NCF 2023 aligned MCQs.

TOPIC:
{topic}

DOCUMENT:
{context}

DIFFICULTY:
{difficulty}

Generate:

# Learning Outcomes

# Competencies

# Easy MCQs

5 Questions

# Moderate MCQs

5 Questions

# Hard MCQs

5 Questions

For every question provide:

- Question
- Options A-D
- Correct Answer
- Explanation
"""

    return call_llm(
        prompt,
        max_tokens=2500
    )


# =====================================================
# QUESTION PAPER GENERATOR
# =====================================================

def generate_document_question_paper(
    topic: str,
    marks: int = 20,
    difficulty: str = "Mixed"
) -> str:

    context = get_context(
        topic,
        top_k=5
    )

    if not context.strip():
        return "No relevant content found in uploaded document."

    prompt = f"""
Generate a complete NCF 2023 aligned question paper.

TOPIC:
{topic}

DOCUMENT:
{context}

TOTAL MARKS:
{marks}

DIFFICULTY:
{difficulty}

Generate:

# Learning Outcomes

# Competencies

SECTION A
Easy Questions

SECTION B
Moderate Questions

SECTION C
Hard Questions

SECTION D
Case Based Questions

SECTION E
Activity Based Questions

Provide:

- Marks Distribution
- Answer Key
- Competency Mapping
"""

    return call_llm(
        prompt,
        max_tokens=2500
    )
