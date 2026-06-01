# ==========================================
# AI TEACHER ASSISTANT PROMPTS
# ==========================================

DEFAULT_SYSTEM_PROMPT = """
You are an AI Teacher Assistant.

IMPORTANT RULES:

1. By default explain everything like a Class 5 student.
2. Use simple words.
3. Use short sentences.
4. Give real-life examples.
5. Avoid difficult technical language.
6. Make learning fun and engaging.
7. If possible use bullet points.
8. If information comes from uploaded documents, prioritize that information.
9. If information comes from web search, mention that the answer was found from web sources.
"""

# ==========================================
# EXPLAIN TOPIC
# ==========================================

EXPLAIN_TOPIC_PROMPT = """
Explain the following topic.

Topic:
{topic}

Student Level:
{student_level}

Teaching Style:
{teaching_style}

Instructions:

- Explain simply.
- Use examples.
- Use easy language.
- Assume the student is in Class 5 unless another level is selected.
- Make it easy to understand.
"""

# ==========================================
# NOTES GENERATOR
# ==========================================

NOTES_PROMPT = """
Create study notes from the following content.

Content:
{content}

Student Level:
{student_level}

Requirements:

- Easy language
- Important points
- Bullet format
- Revision friendly
- Class 5 level by default
"""

# ==========================================
# TOPIC NOTES
# ==========================================

TOPIC_NOTES_PROMPT = """
Create topic-wise notes.

Content:
{content}

Requirements:

- Separate each topic
- Add headings
- Add key points
- Easy explanation
- Student-friendly
"""

# ==========================================
# MCQ GENERATOR
# ==========================================

MCQ_PROMPT = """
Generate {difficulty} MCQs.

Content:
{content}

Requirements:

- Multiple choice questions
- 4 options
- Provide correct answer
- Clear formatting

Difficulty:
{difficulty}

Difficulty Meaning:

Easy:
Knowledge based

Moderate:
Concept understanding

Hard:
Application and analysis

Mixed:
Combination of all levels
"""

# ==========================================
# QUESTION PAPER GENERATOR
# ==========================================

QUESTION_PAPER_PROMPT = """
Generate a question paper.

Content:
{content}

Total Marks:
{marks}

Difficulty:
{difficulty}

Student Level:
{student_level}

Requirements:

- Proper exam format
- Include marks
- Mix question types
- Include short answers
- Include long answers
- Well structured
"""

# ==========================================
# LESSON PLAN
# ==========================================

LESSON_PLAN_PROMPT = """
Create a lesson plan.

Topic:
{topic}

Student Level:
{student_level}

Include:

1. Learning Objective
2. Introduction
3. Teaching Process
4. Classroom Activity
5. Assessment
6. Homework
7. Recap

Make it teacher-friendly.
"""

# ==========================================
# TEACHING GUIDE
# ==========================================

TEACHING_GUIDE_PROMPT = """
Create a teaching guide.

Topic:
{topic}

Student Level:
{student_level}

Teaching Style:
{teaching_style}

Include:

1. How to start the class
2. What teacher should say
3. Real-life examples
4. Student activities
5. Common doubts
6. Homework
7. Recap

Make it practical and easy.
"""

# ==========================================
# HOMEWORK
# ==========================================

HOMEWORK_PROMPT = """
Generate homework.

Topic:
{topic}

Student Level:
{student_level}

Requirements:

- Easy to understand
- Relevant to topic
- Suitable for home practice
"""

# ==========================================
# WORKSHEET
# ==========================================

WORKSHEET_PROMPT = """
Generate a worksheet.

Content:
{content}

Student Level:
{student_level}

Include:

- Fill in the blanks
- Match the following
- True/False
- Short answers

Keep it engaging.
"""

# ==========================================
# BLOOM TAXONOMY
# ==========================================

BLOOM_PROMPT = """
Generate Bloom's Taxonomy questions.

Topic:
{topic}

Create questions for:

1. Remember
2. Understand
3. Apply
4. Analyze
5. Evaluate
6. Create

Student Level:
{student_level}
"""

# ==========================================
# WEB SEARCH ANSWER
# ==========================================

WEB_SEARCH_PROMPT = """
Answer the user's question using the web search content.

Question:
{question}

Web Content:
{web_content}

Requirements:

- Simple explanation
- Mention source is web search
- Class 5 level by default
"""
