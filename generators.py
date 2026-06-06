import streamlit as st
from openai import OpenAI


# ==========================================
# OPENROUTER CLIENT
# ==========================================

def get_client():

    if "OPENROUTER_API_KEY" not in st.secrets:

        raise Exception(
            "OPENROUTER_API_KEY not found in Streamlit Secrets"
        )

    return OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )


# ==========================================
# COMMON LLM FUNCTION
# ==========================================

def call_llm(prompt):

    try:

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
            max_tokens=2500
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Generation Error: {str(e)}"


# ==========================================
# LESSON PLAN GENERATOR
# ==========================================

def generate_lesson_plan(
    topic,
    student_level="Class 5"
):

    prompt = f"""
You are an expert teacher.

Create a complete lesson plan.

Topic:
{topic}

Student Level:
{student_level}

Include:

1. Learning Objectives

2. Introduction

3. Teaching Method

4. Activities

5. Class Discussion

6. Assessment

7. Homework

8. Summary

Make it detailed and classroom ready.
"""

    return call_llm(prompt)


# ==========================================
# TEACHING GUIDE GENERATOR
# ==========================================

def generate_teaching_guide(
    topic,
    student_level="Class 5",
    teaching_style="Beginner Friendly"
):

    prompt = f"""
You are an expert teacher trainer.

Create a teaching guide.

Topic:
{topic}

Student Level:
{student_level}

Teaching Style:
{teaching_style}

Include:

1. Topic Explanation

2. Key Concepts

3. Real Life Examples

4. Classroom Activities

5. Student Questions

6. Assessment Questions

7. Common Mistakes

8. Teaching Tips

Make it practical and easy for teachers.
"""

    return call_llm(prompt)
