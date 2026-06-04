import streamlit as st
from openai import OpenAI


def get_client():
    api_key = st.secrets["OPENROUTER_API_KEY"]

    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )


def call_llm(prompt):

    client = get_client()

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=2000
    )

    return response.choices[0].message.content


def generate_lesson_plan(
    topic,
    student_level="Class 5"
):

    prompt = f"""
Create a lesson plan.

Topic:
{topic}

Student Level:
{student_level}

Include:
- Learning Objectives
- Introduction
- Activities
- Assessment
"""

    return call_llm(prompt)


def generate_teaching_guide(
    topic,
    student_level="Class 5",
    teaching_style="Beginner Friendly"
):

    prompt = f"""
Create a teaching guide.

Topic:
{topic}

Student Level:
{student_level}

Teaching Style:
{teaching_style}

Include:
- Explanation
- Examples
- Activities
- Questions
"""

    return call_llm(prompt)
