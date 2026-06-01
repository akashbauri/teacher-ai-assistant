```python
import streamlit as st

from document_parser import (
    extract_document_text,
    chunk_text,
    get_document_info
)

from chroma_manager import (
    store_document_chunks,
    get_document_count
)

from rag_engine import (
    rag_answer,
    generate_document_notes,
    generate_document_mcqs,
    generate_document_question_paper
)

from generators import (
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
    detect_difficulty,
    detect_marks
)

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="AI Teacher Assistant",
    page_icon="📚",
    layout="wide"
)

initialize_history()

# ======================================
# SIDEBAR
# ======================================

with st.sidebar:

    st.title("📚 AI Teacher Assistant")

    st.markdown("### History")

    history = get_history()

    if history:

        for item in reversed(history[-10:]):

            st.write(
                f"📝 {item['question'][:40]}"
            )

    st.divider()

    st.markdown(
        f"📄 Documents Stored: {get_document_count()}"
    )

# ======================================
# HEADER
# ======================================

st.title("📚 AI Teacher Assistant")

st.markdown("""
### Upload a document and ask anything.

Default:
- Class 5 Friendly
- Source Tracking
- PDF Downloads
- Notes
- MCQs
- Question Papers
- Lesson Plans
- Teaching Guides
""")

# ======================================
# FILE UPLOAD
# ======================================

uploaded_file = st.file_uploader(
    "Upload PDF / DOCX",
    type=["pdf", "docx", "txt"]
)

# ======================================
# PROCESS DOCUMENT
# ======================================

if uploaded_file:

    with st.spinner(
        "Reading document..."
    ):

        text = extract_document_text(
            uploaded_file
        )

        chunks = chunk_text(text)

        store_document_chunks(
            chunks,
            uploaded_file.name
        )

        info = get_document_info(text)

        st.success(
            "Document processed successfully."
        )

        st.info(
            f"""
Words: {info['words']}

Characters: {info['characters']}
"""
        )

# ======================================
# SETTINGS
# ======================================

student_level = st.selectbox(
    "Student Level",
    [
        "Class 5",
        "Class 6-8",
        "Class 9-10",
        "Class 11-12",
        "College"
    ]
)

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

# ======================================
# ACTION
# ======================================

action = st.selectbox(
    "Choose Action",
    [
        "Ask Question",
        "Generate Notes",
        "Generate MCQs",
        "Generate Question Paper",
        "Generate Lesson Plan",
        "Generate Teaching Guide"
    ]
)

# ======================================
# QUERY
# ======================================

query = st.text_area(
    "Enter Topic or Question"
)

# ======================================
# GENERATE
# ======================================

if st.button("🚀 Generate"):

    if not query:

        st.warning(
            "Please enter a topic."
        )

        st.stop()

    result = ""
    source = ""

    with st.spinner(
        "Generating..."
    ):

        try:

            # ----------------------
            # QUESTION ANSWERING
            # ----------------------

            if action == "Ask Question":

                response = rag_answer(
                    query,
                    student_level
                )

                result = response["answer"]

                source = response["source"]

                pdf_data = notes_pdf(
                    result,
                    source
                )

                pdf_name = "answer.pdf"

            # ----------------------
            # NOTES
            # ----------------------

            elif action == "Generate Notes":

                result = generate_document_notes(
                    query,
                    student_level
                )

                source = "Uploaded Document"

                pdf_data = notes_pdf(
                    result,
                    source
                )

                pdf_name = "notes.pdf"

            # ----------------------
            # MCQS
            # ----------------------

            elif action == "Generate MCQs":

                difficulty = detect_difficulty(
                    query
                )

                result = generate_document_mcqs(
                    query,
                    difficulty
                )

                source = "Uploaded Document"

                pdf_data = mcq_pdf(
                    result,
                    source
                )

                pdf_name = "mcqs.pdf"

            # ----------------------
            # QUESTION PAPER
            # ----------------------

            elif action == "Generate Question Paper":

                marks = detect_marks(
                    query
                )

                difficulty = detect_difficulty(
                    query
                )

                result = generate_document_question_paper(
                    query,
                    marks,
                    difficulty
                )

                source = "Uploaded Document"

                pdf_data = question_paper_pdf(
                    result,
                    source
                )

                pdf_name = "question_paper.pdf"

            # ----------------------
            # LESSON PLAN
            # ----------------------

            elif action == "Generate Lesson Plan":

                result = generate_lesson_plan(
                    query,
                    student_level
                )

                source = "Uploaded Document"

                pdf_data = lesson_plan_pdf(
                    result,
                    source
                )

                pdf_name = "lesson_plan.pdf"

            # ----------------------
            # TEACHING GUIDE
            # ----------------------

            elif action == "Generate Teaching Guide":

                result = generate_teaching_guide(
                    query,
                    student_level,
                    teaching_style
                )

                source = "Uploaded Document"

                pdf_data = teaching_guide_pdf(
                    result,
                    source
                )

                pdf_name = "teaching_guide.pdf"

            save_to_history(
                query,
                result,
                source
            )

            st.success(
                "Generated Successfully"
            )

            st.markdown(result)

            st.divider()

            st.subheader(
                "📌 Source"
            )

            st.success(source)

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
```
