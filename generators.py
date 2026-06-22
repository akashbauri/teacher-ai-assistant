# ==========================================
# generators.py
# ==========================================

from llm_service import call_llm


# ==========================================
# COMMON GENERATOR
# ==========================================

def generate_content(
    prompt,
    max_tokens=1500
):
    """
    Common wrapper for all generators.
    """

    return call_llm(
        prompt,
        max_tokens
    )


# ==========================================
# LEARNING OUTCOMES
# ==========================================

def generate_learning_outcomes(
    topic,
    student_level="Class 5"
):

    prompt = f"""
Generate NCF 2023 aligned Learning Outcomes.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

Generate:

# Knowledge Outcomes

# Skill Outcomes

# Application Outcomes

# Assessment Indicators

Use action verbs:

- Explain
- Identify
- Compare
- Analyze
- Apply
- Evaluate
- Create
"""

    return generate_content(
        prompt,
        1200
    )


# ==========================================
# COMPETENCIES
# ==========================================

def generate_competencies(
    topic,
    student_level="Class 5"
):

    prompt = f"""
Generate NCF 2023 aligned competencies.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

Include:

# Critical Thinking

# Communication

# Problem Solving

# Collaboration

# Observation

# Creativity

# Reasoning

Explain each competency briefly.
"""

    return generate_content(
        prompt,
        1200
    )


# ==========================================
# LESSON PLAN
# ==========================================

def generate_lesson_plan(
    topic,
    student_level="Class 5"
):

    prompt = f"""
Create a complete NCF 2023 aligned lesson plan.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

Generate:

# Topic Information

# Learning Outcomes

# Competencies

# Prior Knowledge

# Teaching Learning Materials

# Activity Based Learning

# Teacher Explanation Script

# Step By Step Teaching Procedure

# Real Life Applications

# Inclusive Teaching Strategies

# Assessment

# Reflection

# Homework

# Flow Chart

# Mind Map

Use teacher-friendly language.
"""

    return generate_content(
        prompt,
        2200
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
Create a complete NCF 2023 aligned teaching guide.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

TEACHING STYLE:
{teaching_style}

Generate:

# Chapter Overview

# Learning Outcomes

# Competencies

# Key Concepts

# Teacher Introduction Script

# Detailed Topic Explanation

# Real Life Examples

# Activity Based Learning

# Student Engagement Questions

# Common Misconceptions

# Inclusive Teaching Strategies

# Easy Questions

# Moderate Questions

# Hard Questions

# Assessment Suggestions

# Extension Activities

# Homework

# Recap

# Flow Chart

# Mind Map

Explain as if training a teacher.
"""

    return generate_content(
        prompt,
        2500
    )


# ==========================================
# FLOWCHART
# ==========================================

def generate_flowchart(
    topic
):

    prompt = f"""
Generate an NCF 2023 aligned educational flowchart.

TOPIC:
{topic}

Structure:

Prerequisite Knowledge
↓
Introduction
↓
Core Concept
↓
Teacher Explanation
↓
Activity
↓
Discussion
↓
Application
↓
Assessment
↓
Reflection

Use arrows and clean formatting.
"""

    return generate_content(
        prompt,
        1200
    )


# ==========================================
# MIND MAP
# ==========================================

def generate_mindmap(
    topic
):

    prompt = f"""
Generate an NCF 2023 aligned educational mind map.

TOPIC:
{topic}

Include:

Central Topic

├── Core Concepts
├── Learning Outcomes
├── Competencies
├── Real Life Applications
├── Activity Ideas
├── Assessment Ideas
└── Cross Curricular Connections

Use proper hierarchical structure.
"""

    return generate_content(
        prompt,
        1200
    )


# ==========================================
# CHAPTER SUMMARY
# ==========================================

def generate_chapter_summary(
    topic
):

    prompt = f"""
Generate an NCF 2023 aligned chapter summary.

TOPIC:
{topic}

Include:

# Chapter Overview

# Learning Outcomes

# Competencies

# Key Concepts

# Important Definitions

# Important Formulas

# Real Life Applications

# Quick Revision Notes

# Summary

Use simple language.
"""

    return generate_content(
        prompt,
        1500
    )


# ==========================================
# IMPORTANT QUESTIONS
# ==========================================

def generate_important_questions(
    topic
):

    prompt = f"""
Generate NCF 2023 aligned important questions.

TOPIC:
{topic}

Generate:

# Easy Questions
(Knowledge)

# Moderate Questions
(Understanding & Application)

# Hard Questions
(Analysis & Evaluation)

# Competency Based Questions

# Activity Based Questions

# Case Based Questions

Provide:

10 Easy Questions
10 Moderate Questions
10 Hard Questions
"""

    return generate_content(
        prompt,
        2200
    )
