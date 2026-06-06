import streamlit as st

# Document Processing
from document_parser import (
    extract_document_text,
    chunk_text,
    get_document_info
)

# Vector Database
from chroma_manager import (
    store_document_chunks,
    get_document_count
)

# RAG Engine
from rag_engine import (
    rag_answer,
    generate_document_notes,
    generate_document_mcqs,
    generate_document_question_paper
)

# Content Generators
from generators import (
    generate_lesson_plan,
    generate_teaching_guide
)

# PDF Generators
from pdf_generator import (
    notes_pdf,
    mcq_pdf,
    question_paper_pdf,
    lesson_plan_pdf,
    teaching_guide_pdf
)

# Utilities
from utils import (
    initialize_history,
    save_to_history,
    get_history,
    detect_difficulty,
    detect_marks,
    search_web,
    format_web_results
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Teacher Assistant",
    page_icon="📚",
    layout="wide"
)

initialize_history()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📚 AI Teacher Assistant")

    st.markdown("### Recent History")

    history = get_history()

    if history:
        for item in reversed(history[-10:]):
            st.write(
                f"📝 {item['question'][:40]}"
            )

    st.divider()

    doc_count = get_document_count()

    st.markdown(
        f"📄 Documents Stored: {doc_count}"
    )

    if doc_count > 0:
        st.success("✅ Vector Database Active")
    else:
        st.warning("⚠️ No Document Indexed")

# =====================================================
# HEADER
# =====================================================

st.title("📚 AI Teacher Assistant")

st.markdown("""
### Upload a document and ask anything.

#### Features
- PDF / DOCX / TXT Upload
- ChromaDB Vector Search
- AI Question Answering
- Notes Generator
- MCQ Generator
- Question Paper Generator
- Lesson Plan Generator
- Teaching Guide Generator
- Web Search
- PDF Download
""")

# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload PDF / DOCX / TXT",
    type=["pdf", "docx", "txt"]
)

# =====================================================
# DOCUMENT PROCESSING
# =====================================================

if uploaded_file:

    if (
        "last_uploaded_file" not in st.session_state
        or
        st.session_state["last_uploaded_file"]
        != uploaded_file.name
    ):

        with st.spinner("Processing document..."):

            text = extract_document_text(
                uploaded_file
            )

            chunks = chunk_text(text)

            store_document_chunks(
                chunks,
                uploaded_file.name
            )

            st.session_state[
                "last_uploaded_file"
            ] = uploaded_file.name

            info = get_document_info(text)

            st.success(
                "Document Processed Successfully!"
            )

            st.info(
                f"""
Words: {info['words']}

Characters: {info['characters']}
"""
            )

            st.subheader("📖 Document Preview")

            st.text_area(
                "Preview",
                text[:2000],
                height=250
            )

# =====================================================
# SETTINGS
# =====================================================

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

# =====================================================
# ACTION SELECTION
# =====================================================

action = st.selectbox(
    "Choose Action",
    [
        "Ask Question",
        "Generate Notes",
        "Generate MCQs",
        "Generate Question Paper",
        "Generate Lesson Plan",
        "Generate Teaching Guide",
        "Web Search"
    ]
)

# =====================================================
# QUERY INPUT
# =====================================================

query = st.text_area(
    "Enter Topic or Question"
)

# =====================================================
# GENERATE BUTTON
# =====================================================

if st.button("🚀 Generate"):

    if not query:
        st.warning("Please enter a topic.")
        st.stop()

    result = ""
    source = ""

    try:

        with st.spinner("Generating..."):

            # Ask Question
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

            # Notes
            elif action == "Generate Notes":

                result = generate_document_notes(
                    query,
                    student_level
                )

                source = (
                    uploaded_file.name
                    if uploaded_file
                    else "Document"
                )

                pdf_data = notes_pdf(
                    result,
                    source
                )

                pdf_name = "notes.pdf"

            # MCQs
            elif action == "Generate MCQs":

                difficulty = detect_difficulty(
                    query
                )

                result = generate_document_mcqs(
                    query,
                    difficulty
                )

                source = (
                    uploaded_file.name
                    if uploaded_file
                    else "Document"
                )

                pdf_data = mcq_pdf(
                    result,
                    source
                )

                pdf_name = "mcqs.pdf"

            # Question Paper
            elif action == "Generate Question Paper":

                marks = detect_marks(query)

                difficulty = detect_difficulty(
                    query
                )

                result = generate_document_question_paper(
                    query,
                    marks,
                    difficulty
                )

                source = (
                    uploaded_file.name
                    if uploaded_file
                    else "Document"
                )

                pdf_data = question_paper_pdf(
                    result,
                    source
                )

                pdf_name = "question_paper.pdf"

            # Lesson Plan
            elif action == "Generate Lesson Plan":

                result = generate_lesson_plan(
                    query,
                    student_level
                )

                source = (
                    uploaded_file.name
                    if uploaded_file
                    else "Document"
                )

                pdf_data = lesson_plan_pdf(
                    result,
                    source
                )

                pdf_name = "lesson_plan.pdf"

            # Teaching Guide
            elif action == "Generate Teaching Guide":

                result = generate_teaching_guide(
                    query,
                    student_level,
                    teaching_style
                )

                source = (
                    uploaded_file.name
                    if uploaded_file
                    else "Document"
                )

                pdf_data = teaching_guide_pdf(
                    result,
                    source
                )

                pdf_name = "teaching_guide.pdf"

            # Web Search
            elif action == "Web Search":

                results = search_web(query)

                result = format_web_results(
                    results
                )

                source = "Web Search"

                pdf_data = notes_pdf(
                    result,
                    source
                )

                pdf_name = "web_search.pdf"

            save_to_history(
                query,
                result,
                source
            )

            st.success(
                "Generated Successfully!"
            )

            st.markdown(result)

            st.divider()

            st.subheader("📌 Source")
            st.info(source)

            st.download_button(
                label="📄 Download PDF",
                data=pdf_data,
                file_name=pdf_name,
                mime="application/pdf"
            )

    except Exception as e:
        st.exception(e)
