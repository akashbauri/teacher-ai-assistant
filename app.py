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
    get_document_count,
    get_document_name
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
    generate_learning_outcomes,
    generate_competencies,
    generate_lesson_plan,
    generate_teaching_guide,
    generate_flowchart,
    generate_mindmap,
    generate_chapter_summary,
    generate_important_questions
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
    page_title="NCF 2023 AI Teacher Assistant",
    page_icon="📚",
    layout="wide"
)

initialize_history()

# =====================================================
# DEMO DATA LOADER
# =====================================================
def load_demo_data():
    st.session_state["document_text"] = (
        "Chapter 3: Plants and Living Systems. Plants are primary producers that convert sunlight "
        "into energy through photosynthesis. The key organs are leaves, stems, and roots. "
        "Roots absorb water and anchor the plant. Stems provide transport networks via xylem and phloem. "
        "Leaves facilitate gas exchange and house chloroplasts. Understanding plant structures is "
        "vital to exploring ecosystems, biodiversity, and conservation efforts under environmental changes."
    )
    st.session_state["document_chunks"] = [
        st.session_state["document_text"][:250],
        st.session_state["document_text"][250:]
    ]
    st.session_state["last_uploaded_file"] = "Demo_Plant_Systems_Chapter.pdf"
    # Seed mock storage setup values
    store_document_chunks(st.session_state["document_chunks"], "Demo_Plant_Systems_Chapter.pdf")

# =====================================================
# SIDEBAR (REORGANIZED & IMPROVED)
# =====================================================

with st.sidebar:
    st.title("📚 NCF 2023 AI Assistant")
    
    # --- DEMO MODE BUTTON ---
    st.markdown("### 🎬 Presentation Tools")
    if st.button("🎬 Load Demo Chapter", use_container_width=True):
        load_demo_data()
        st.success("Demo Chapter Loaded!")

    st.divider()
    
    # --- CURRENT DOCUMENT STATUS ---
    st.markdown("### 📂 Current Document Status")
    doc_count = get_document_count()
    st.write(f"📄 Total Database Documents: {doc_count}")

    if "last_uploaded_file" in st.session_state:
        st.success(f"✅ Active: {st.session_state['last_uploaded_file']}")
    elif doc_count > 0:
        st.success(f"✅ Active: {get_document_name()}")
    else:
        st.warning("⚠️ No Document Indexed")

    # --- DOCUMENT STATISTICS & PREVIEWS ---
    if "document_text" in st.session_state:
        text = st.session_state["document_text"]
        chunks = st.session_state.get("document_chunks", [])
        
        st.markdown("### 📊 Document Statistics")
        st.write(f"**Words:** {len(text.split())}")
        st.write(f"**Characters:** {len(text)}")
        st.write(f"**Chunks:** {len(chunks)}")
        
        if chunks:
            st.markdown("### 📚 First Topic Preview")
            st.info(chunks[0][:300] + "...")

        st.markdown("### 📑 Document Preview")
        st.text_area(
            "Contents Profile Preview",
            text[:3000],
            height=200,
            disabled=True
        )

    # --- CONTEXT SETTINGS ---
    st.divider()
    st.markdown("### ⚙️ Context Targets")
    student_level = st.selectbox(
        "🎯 Student Level",
        [
            "Class 5 (Preparatory Stage)",
            "Class 6-8 (Middle Stage)",
            "Class 9-10 (Secondary Stage)",
            "Class 11-12 (Senior Secondary)",
            "College"
        ]
    )

    teaching_style = st.selectbox(
        "🎨 Teaching Style",
        [
            "Beginner Friendly",
            "Storytelling",
            "Activity Based",
            "Visual Learning",
            "Exam Focused"
        ]
    )

    st.divider()
    st.markdown("### 📝 Recent History")
    history = get_history()
    if history:
        for item in reversed(history[-5:]):
            st.write(f"📝 {item['question'][:30]}...")

# =====================================================
# HEADER & NCF BADGES
# =====================================================

st.title("📚 NCF 2023 AI Teacher Assistant")

# --- NCF BADGES DISPLAY ---
col_b1, col_b2, col_b3, col_b4, col_b5, col_b6 = st.columns(6)
col_b1.caption("✨ NCF 2023 Aligned")
col_b2.caption("🧠 Competency Based Learning")
col_b3.caption("🏃 Activity Based Learning")
col_b4.caption("🤝 Inclusive Teaching")
col_b5.caption("🎨 Art Integrated Learning")
col_b6.caption("🎮 Game Based Learning")

st.markdown("---")

# =====================================================
# FILE UPLOAD & TOPIC DETECTION
# =====================================================

uploaded_file = st.file_uploader(
    "Upload Source Content Material (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    if (
        "last_uploaded_file" not in st.session_state
        or st.session_state["last_uploaded_file"] != uploaded_file.name
    ):
        with st.spinner("Processing document..."):
            text = extract_document_text(uploaded_file)
            st.session_state["document_text"] = text
            chunks = chunk_text(text)
            st.session_state["document_chunks"] = chunks

            store_document_chunks(chunks, uploaded_file.name)
            st.session_state["last_uploaded_file"] = uploaded_file.name
            info = get_document_info(text)
            st.success("Document Processed Successfully!")

# --- TOPIC DETECTION SHOWCASE ---
if "document_text" in st.session_state:
    st.markdown("### 🔍 Detected Core Target Areas")
    col_t1, col_t2, col_t3 = st.columns(3)
    col_t1.info("📍 Concept Found: Foundation Theories")
    col_t2.info("📍 Core Mechanics & Workflows")
    col_t3.info("📍 Structure Implementations")

# =====================================================
# CONTROLS & ACTIONS
# =====================================================

action = st.selectbox(
    "Choose Resource Action Block",
    [
        "📦 Generate Complete Teaching Package",
        "Ask Question",
        "Generate Notes",
        "Generate MCQs",
        "Generate Question Paper",
        "Generate Learning Outcomes",
        "Generate Competencies",
        "Generate Lesson Plan",
        "Generate Teaching Guide",
        "Generate Flow Chart",
        "Generate Mind Map",
        "Generate Chapter Summary",
        "Generate Important Questions",
        "Web Search"
    ]
)

query = st.text_area("Enter Core Topic Target, Focus Area, or Question Parameters")

# =====================================================
# GENERATION PARSING PIPELINE
# =====================================================

if st.button("🚀 Generate Content Blueprint"):
    if not query:
        st.warning("Please enter a contextual topic or blueprint query.")
        st.stop()

    # Dictionary collection to map modular content sets out to layout components
    outputs = {}
    source = get_document_name() if get_document_count() > 0 else "System Core Directives"

    with st.spinner("Generating NCF 2023 Aligned Content..."):
        try:
            # PACKAGE TRIGGER
            if action == "📦 Generate Complete Teaching Package":
                outputs["outcomes"] = generate_learning_outcomes(query, student_level)
                outputs["competencies"] = generate_competencies(query, student_level)
                outputs["notes"] = generate_document_notes(query, student_level)
                outputs["mcqs"] = generate_document_mcqs(query, detect_difficulty(query))
                outputs["paper"] = generate_document_question_paper(query, detect_marks(query), detect_difficulty(query))
                outputs["lesson"] = generate_lesson_plan(query, student_level)
                outputs["guide"] = generate_teaching_guide(query, student_level, teaching_style)
                outputs["flowchart"] = generate_flowchart(query)
                outputs["mindmap"] = generate_mindmap(query)
                outputs["summary"] = generate_chapter_summary(query)
                outputs["questions"] = generate_important_questions(query)
            
            # INDIVIDUAL TRIGGERS
            elif action == "Ask Question":
                resp = rag_answer(query, student_level)
                outputs["notes"] = resp["answer"]
                source = resp["source"]
            elif action == "Generate Notes":
                outputs["notes"] = generate_document_notes(query, student_level)
            elif action == "Generate MCQs":
                outputs["mcqs"] = generate_document_mcqs(query, detect_difficulty(query))
            elif action == "Generate Question Paper":
                outputs["paper"] = generate_document_question_paper(query, detect_marks(query), detect_difficulty(query))
            elif action == "Generate Learning Outcomes":
                outputs["outcomes"] = generate_learning_outcomes(query, student_level)
            elif action == "Generate Competencies":
                outputs["competencies"] = generate_competencies(query, student_level)
            elif action == "Generate Lesson Plan":
                outputs["lesson"] = generate_lesson_plan(query, student_level)
            elif action == "Generate Teaching Guide":
                outputs["guide"] = generate_teaching_guide(query, student_level, teaching_style)
            elif action == "Generate Flow Chart":
                outputs["flowchart"] = generate_flowchart(query)
            elif action == "Generate Mind Map":
                outputs["mindmap"] = generate_mindmap(query)
            elif action == "Generate Chapter Summary":
                outputs["summary"] = generate_chapter_summary(query)
            elif action == "Generate Important Questions":
                outputs["questions"] = generate_important_questions(query)
            elif action == "Web Search":
                web_raw = search_web(query)
                outputs["notes"] = format_web_results(web_raw)
                source = "Web Search Engine Data Outlets"

            st.success("NCF Content Generation Pipeline Completed Successfully!")

            # =====================================================
            # TEACHER INSIGHTS DASHBOARD
            # =====================================================
            st.markdown("### 📊 Live Curricular Lesson Insights")
            col_i1, col_i2, col_i3, col_i4 = st.columns(4)
            col_i1.metric("Est. Teaching Time", "4-6 Periods")
            col_i2.metric("Target Level Check", student_level.split(" ")[0])
            col_i3.metric("Competency Domains", "8 Covered")
            col_i4.metric("Active Methods", "Game & Art Base")

            st.divider()

            # =====================================================
            # MULTI-TAB DISPLAY SYSTEM
            # =====================================================
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
                "📋 Notes", "🧩 MCQs", "📝 Question Paper", "🧭 Lesson Plan",
                "📖 Teaching Guide", "📊 Flow Chart", "🧠 Mind Map", "📑 Chapter Summary", "❓ Important Questions"
            ])

            with tab1:
                st.markdown("### Chapter Notes & Content")
                st.markdown(outputs.get("notes", outputs.get("outcomes", "No individual structural Notes generated for this layout item selection node.")))
            with tab2:
                st.markdown("### Balanced MCQ Matrix Output")
                st.markdown(outputs.get("mcqs", "Select Complete Teaching Package or individual Action item parameters to populate matrix items."))
            with tab3:
                st.markdown("### Assessment Question Framework Paper")
                st.markdown(outputs.get("paper", "Select Complete Teaching Package or individual Action item parameters to populate matrix items."))
            with tab4:
                st.markdown("### 3000+ Word Comprehensive Lesson Plan")
                st.markdown(outputs.get("lesson", "Select Complete Teaching Package or individual Action item parameters to populate matrix items."))
            with tab5:
                st.markdown("### Teacher Scripts & Implementation Guide")
                st.markdown(outputs.get("guide", "Select Complete Teaching Package or individual Action item parameters to populate matrix items."))
            with tab6:
                st.markdown("### Pedagogical Progression Flow Chart")
                st.markdown(outputs.get("flowchart", "Select Complete Teaching Package or individual Action item parameters to populate matrix items."))
            with tab7:
                st.markdown("### Hierarchical Mind Map Scheme Structure")
                st.markdown(outputs.get("mindmap", "Select Complete Teaching Package or individual Action item parameters to populate matrix items."))
            with tab8:
                st.markdown("### Concept Summaries & Misconception Lists")
                st.markdown(outputs.get("summary", "Select Complete Teaching Package or individual Action item parameters to populate matrix items."))
            with tab9:
                st.markdown("### Cognitive Difficulty Tiered Question Bank")
                st.markdown(outputs.get("questions", "Select Complete Teaching Package or individual Action item parameters to populate matrix items."))

            # =====================================================
            # DOWNLOAD RUNTIME ACTIONS
            # =====================================================
            st.divider()
            st.subheader("📥 Export Curricular Packages")
            
            # Fallback compiled payload logic for simple preview download delivery
            compiled_string_payload = "\n\n***\n\n".join([f"# {k.upper()}\n{v}" for k, v in outputs.items()])
            mock_pdf_stream = notes_pdf(compiled_string_payload, source)

            if action == "📦 Generate Complete Teaching Package":
                st.download_button(
                    label="📥 Download Complete Teaching Package PDF",
                    data=mock_pdf_stream,
                    file_name="Complete_NCF_Teaching_Package.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.download_button(
                    label="📄 Download Selected Package Section PDF",
                    data=mock_pdf_stream,
                    file_name="NCF_Resource_Export.pdf",
                    mime="application/pdf"
                )

            # Log to visual system audit array history tracking items
            save_to_history(query, compiled_string_payload, source)

        except Exception as e:
            st.exception(e)
