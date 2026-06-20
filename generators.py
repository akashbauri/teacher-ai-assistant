from groq import Groq

from config import (
    GROQ_API_KEY
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
# LESSON PLAN
# ==========================================

def generate_lesson_plan(
    topic,
    student_level="Class 5"
):

    prompt = f"""
You are an expert teacher.

Create a complete lesson plan.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

Include:

# Learning Objectives

# Introduction

# Teaching Method

# Classroom Activities

# Assessment

# Homework

# Summary

# Flow Chart

# Mind Map

Make it classroom ready.
"""

    return call_llm(
        prompt,
        1500
    )


# ==========================================
# TEACHING GUIDE
# ==========================================

def generate_teaching_guide(
    topic,
    student_level="Class 5",
    teaching_style="Beginner Friendly"
):

    prompt = f"""
You are an expert teacher trainer.

Create a teaching guide.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

TEACHING STYLE:
{teaching_style}

Include:

# Topic Explanation

# Key Concepts

# Real Life Examples

# Classroom Activities

# Student Questions

# Assessment Questions

# Common Mistakes

# Teaching Tips

# Flow Chart

# Mind Map

Make it practical and easy to teach.
"""

    return call_llm(
        prompt,
        1500
    )


# ==========================================
# FLOWCHART GENERATOR
# ==========================================

def generate_flowchart(
    topic
):

    prompt = f"""
Create a detailed educational flowchart.

TOPIC:
{topic}

Rules:

- Use arrows
- Step-by-step structure
- Easy for students

Example:

Topic
↓
Step 1
↓
Step 2
↓
Step 3
"""

    return call_llm(
        prompt,
        1000
    )


# ==========================================
# MIND MAP GENERATOR
# ==========================================

def generate_mindmap(
    topic
):

    prompt = f"""
Create an educational mind map.

TOPIC:
{topic}

Format:

Topic
├── Concept 1
├── Concept 2
├── Concept 3
└── Concept 4

Keep it clean and exam focused.
"""

    return call_llm(
        prompt,
        1000
    )


# ==========================================
# CHAPTER SUMMARY
# ==========================================

def generate_chapter_summary(
    topic
):

    prompt = f"""
Create a chapter summary.

TOPIC:
{topic}

Include:

# Key Concepts

# Important Definitions

# Important Formulas

# Exam Points

# Quick Revision Notes

Keep it concise.
"""

    return call_llm(
        prompt,
        1200
    )


# ==========================================
# IMPORTANT QUESTIONS
# ==========================================

def generate_important_questions(
    topic
):

    prompt = f"""
Generate important exam questions.

TOPIC:
{topic}

Include:

- Very Short Questions
- Short Questions
- Long Questions
- HOTS Questions

Provide at least 20 questions.
"""

    return call_llm(
        prompt,
        1200
    )
