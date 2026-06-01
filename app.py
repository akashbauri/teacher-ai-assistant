# app.py

```python
import streamlit as st
from datetime import datetime

from generators import (
    explain_topic,
    generate_notes,
    generate_mcqs,
    generate_question_paper,
    generate_lesson_plan,
    generate_teaching_guide
)

from pdf_generator import (
    notes_pdf,
    mcq_pdf,
    question_paper_pdf,
    lesson_plan_pdf,
    teaching_guide_pdf
)

from utils import (
    initialize_history,
    save_to_history,
    get_history,
    detect_action,
    detect_marks,
    detect_difficulty,
    build_source_label
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Teacher Assistant",
    page_icon="📚",
    layout="wide"
)

initialize_history()

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("📚 AI Teacher Assistant")

    st.markdown("### History")

    history = get_history()

    if len(history) == 0:
        st.info("No history available")

    else:

        for item in reversed(history[-10:]):

            st.write(
                f"📝 {item['question'][:50]}"
            )

# ==========================================
# HEADER
# ==========================================

st.title("📚 AI Teacher Assistant")

st.markdown("""
Upload a document and ask anything.

Default Behavior:

✅ Explain like Class 5 Student

✅ Generate Notes

✅ Generate MCQs

✅ Generate Question Papers

✅ Generate Lesson Plans

✅ Generate Teaching Guides

✅ PDF Download
""")

# ==========================================
# FILE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["pdf", "docx", "pptx", "png", "jpg", "jpeg"]
)

# ==========================================
# SETTINGS
# ==========================================

col1, col2 = st.columns(2)

with col1:

    student_level = st.selectbox(
        "Student Level",
        [
            "Class 5",
            "Class 1-3",
            "Class 6-8",
            "Class 9-10",
            "Class 11-12",
            "College"
        ]
    )

with col2:

    teaching_style = st.selectbox(
        "Teaching Style",
        [
            "Beginner Friendly",
            "Storytelling",
            "Activity Based",
            "Visual Learning",
            "Exam Focused"
        ]
    )

# ==========================================
# QUICK ACTIONS
# ==========================================

st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    explain_btn = st.button("📘 Explain Topic")

with col2:
    notes_btn = st.button("📝 Generate Notes")

with col3:
    mcq_btn = st.button("❓ Generate MCQs")

col4, col5, col6 = st.columns(3)

with col4:
    qp_btn = st.button("📄 Question Paper")

with col5:
    lesson_btn = st.button("📅 Lesson Plan")

with col6:
    guide_btn = st.button("👨‍🏫 Teaching Guide")

# ==========================================
# USER INPUT
# ==========================================

query = st.text_area(
    "Ask Anything",
    height=150
)

# ==========================================
# MAIN GENERATE BUTTON
# ==========================================

if st.button("🚀 Generate"):

    if query.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    action = detect_action(query)

    result = ""

    with st.spinner("Generating..."):

        try:

            if action == "notes":

                result = generate_notes(
                    query,
                    student_level
                )

                pdf_data = notes_pdf(
                    result,
                    "Uploaded Document"
                )

                pdf_name = "notes.pdf"

            elif action == "mcqs":

                difficulty = detect_difficulty(query)

                result = generate_mcqs(
                    query,
                    difficulty
                )

                pdf_data = mcq_pdf(
                    result,
                    "Uploaded Document"
                )

                pdf_name = "mcqs.pdf"

            elif action == "question paper":

                marks = detect_marks(query)

                difficulty = detect_difficulty(query)

                result = generate_question_paper(
                    query,
                    marks,
                    difficulty,
                    student_level
                )

                pdf_data = question_paper_pdf(
                    result,
                    "Uploaded Document"
                )

                pdf_name = "question_paper.pdf"

            elif action == "lesson plan":

                result = generate_lesson_plan(
                    query,
                    student_level
                )

                pdf_data = lesson_plan_pdf(
                    result,
                    "Uploaded Document"
                )

                pdf_name = "lesson_plan.pdf"

            elif action == "teaching guide":

                result = generate_teaching_guide(
                    query,
                    student_level,
                    teaching_style
                )

                pdf_data = teaching_guide_pdf(
                    result,
                    "Uploaded Document"
                )

                pdf_name = "teaching_guide.pdf"

            else:

                result = explain_topic(
                    query,
                    student_level,
                    teaching_style
                )

                pdf_data = notes_pdf(
                    result,
                    "Uploaded Document"
                )

                pdf_name = "explanation.pdf"

            save_to_history(
                query,
                result,
                "Uploaded Document"
            )

            st.success("Generated Successfully")

            st.markdown(result)

            st.divider()

            st.subheader("📌 Source")

            st.success(
                build_source_label(
                    document_used=True
                )
            )

            st.download_button(
                label="📄 Download PDF",
                data=pdf_data,
                file_name=pdf_name,
                mime="application/pdf"
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

# ==========================================
# QUICK ACTIONS
# ==========================================

if explain_btn:
    st.info("Type a topic and click Generate")

if notes_btn:
    st.info("Type Generate Notes and click Generate")

if mcq_btn:
    st.info("Type Generate MCQs and click Generate")

if qp_btn:
    st.info("Type Generate Question Paper and click Generate")

if lesson_btn:
    st.info("Type Create Lesson Plan and click Generate")

if guide_btn:
    st.info("Type Create Teaching Guide and click Generate")

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    f"AI Teacher Assistant | {datetime.now().strftime('%Y-%m-%d')}"
)
```
