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

# 3. Competencies

Generate detailed competency mapping aligned with NCF 2023.

For each competency include:

* Competency Description
* Classroom Application
* Student Behaviour Indicators
* Assessment Evidence

## Critical Thinking

Explain how students analyze, compare, infer, classify, evaluate, and draw conclusions.

## Problem Solving

Explain how students apply concepts to solve real-life situations and classroom challenges.

## Communication Skills

Explain how students express ideas through speaking, writing, discussion, presentation, and visual communication.

## Collaboration

Explain how students work effectively in pairs, teams, and group activities.

## Creativity and Innovation

Explain how students generate ideas, design projects, create models, and develop original solutions.

## Self Learning

Explain how students independently explore concepts and reflect on their own learning.

## Digital Literacy

Explain how students use technology responsibly and effectively for learning.

## Observation and Inquiry

Explain how students observe, investigate, explore, and ask meaningful questions.

# Art Integrated Learning Competency

Explain how art helps students understand the topic through creative expression.

Generate:

* Drawing Activity
* Coloring Activity
* Poster Making Activity
* Craft Activity
* Storytelling Activity
* Drama / Role Play Activity

For each activity provide:

* Objective
* Materials Required
* Procedure
* Expected Learning Outcome

# Game Based Learning Competency

Explain how games help students learn through play, participation, and engagement.

Generate:

## Individual Game

Include:

* Game Name
* Rules
* Learning Objective
* Assessment Method

## Pair Activity Game

Include:

* Game Name
* Rules
* Learning Objective
* Assessment Method

## Group Activity Game

Include:

* Game Name
* Rules
* Learning Objective
* Assessment Method

## Classroom Challenge

Include:

* Challenge Name
* Procedure
* Learning Objective
* Assessment Method

## Quiz Competition

Include:

* Quiz Format
* Rules
* Learning Objective
* Assessment Method

# Real Life Application Competency

Generate at least 10 practical real-life applications.

Explain how students can connect the concept to daily life, community, environment, home, school, and future learning.

IMPORTANT:

Art Integrated Learning and Game Based Learning are mandatory.

Generate detailed classroom-ready activities.

Do not give generic answers.

Provide practical examples that teachers can directly use in the classroom.


    return generate_content(
        prompt,
        3200
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
        2200
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
        2200
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
        2500
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
        3200
    )
