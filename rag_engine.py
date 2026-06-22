# ==========================================
# rag_engine.py
# ==========================================

import traceback

from chroma_manager import get_context

from utils import (
    search_web,
    format_web_results
)

from llm_service import call_llm


# ==========================================
# COMMON DOCUMENT CHECK
# ==========================================

def get_document_context(
    query,
    top_k=5
):
    """
    Retrieve context from ChromaDB.
    """

    context = get_context(
        query,
        top_k=top_k
    )

    return context.strip()


# ==========================================
# EDUCATION PROMPT BUILDER
# ==========================================

def build_education_prompt(
    topic,
    context,
    student_level
):

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

Focus on conceptual understanding.
"""


# ==========================================
# QUESTION ANSWERING
# ==========================================

def rag_answer(
    question,
    student_level="Class 5"
):

    try:

        # -----------------------------
        # ChromaDB Search
        # -----------------------------

        context = get_document_context(
            question
        )

        if context:

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

        # -----------------------------
        # Web Search Fallback
        # -----------------------------

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


# ==========================================
# NOTES GENERATOR
# ==========================================

def generate_document_notes(
    topic,
    student_level="Class 5"
):

    context = get_document_context(
        topic
    )

    if not context:

        return (
            "No relevant content found "
            "in uploaded document."
        )

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

Explain as a teacher.
"""

    return call_llm(
        prompt,
        max_tokens=2200
    )


# ==========================================
# MCQ GENERATOR
# ==========================================

def generate_document_mcqs(
    topic,
    difficulty="Mixed"
):

    context = get_document_context(
        topic
    )

    if not context:

        return (
            "No relevant content found "
            "in uploaded document."
        )

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
(Knowledge)

5 Questions

# Moderate MCQs
(Understanding & Application)

5 Questions

# Hard MCQs
(Analysis & Evaluation)

5 Questions

For every question provide:

Question

Options A-D

Correct Answer

Explanation

Avoid rote memorization.
"""

    return call_llm(
        prompt,
        max_tokens=2500
    )


# ==========================================
# QUESTION PAPER GENERATOR
# ==========================================

def generate_document_question_paper(
    topic,
    marks=20,
    difficulty="Mixed"
):

    context = get_document_context(
        topic
    )

    if not context:

        return (
            "No relevant content found "
            "in uploaded document."
        )

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

Focus on conceptual understanding.
"""

    return call_llm(
        prompt,
        max_tokens=2500
    )
