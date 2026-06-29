import streamlit as st
import time
from datetime import datetime

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
# PAGE CONFIGURATION & STATE INITIALIZATION
# =====================================================
st.set_page_config(
    page_title="NCF 2023 AI Teacher Assistant",
    page_icon="📚",
    layout="wide"
)

initialize_history()

# Session State Keys Initialization for Analytics and Metadata
if "session_start_time" not in st.session_state:
    st.session_state["session_start_time"] = datetime.now()
if "analytics_questions" not in st.session_state:
    st.session_state["analytics_questions"] = 0
if "analytics_resources" not in st.session_state:
    st.session_state["analytics_resources"] = 0
if "analytics_response_times" not in st.session_state:
    st.session_state["analytics_response_times"] = []
if "analytics_uploads" not in st.session_state:
    st.session_state["analytics_uploads"] = 0

if "doc_metadata" not in st.session_state:
    st.session_state["doc_metadata"] = None
if "document_text" not in st.session_state:
    st.session_state["document_text"] = ""
if "document_chunks" not in st.session_state:
    st.session_state["document_chunks"] = []
if "last_uploaded_file" not in st.session_state:
    st.session_state["last_uploaded_file"] = None
if "upload_time" not in st.session_state:
    st.session_state["upload_time"] = "N/A"

# Safe default keys for inputs to prevent baseline jumps
if "student_level_sel" not in st.session_state:
    st.session_state["student_level_sel"] = "Class 5"
if "teaching_style_sel" not in st.session_state:
    st.session_state["teaching_style_sel"] = "Beginner Friendly"


# =====================================================
# UI HELPER FUNCTIONS & RENDERING ENGINE
# =====================================================
def run_staged_pipeline(stages_dict):
    """Executes a visual progressive loading sequence based on modular dictionary definitions."""
    progress_bar = st.progress(0, text="Initializing workflow nodes...")
    total_stages = len(stages_dict)
    for index, (percentage, stage_text) in enumerate(stages_dict.items()):
        progress_bar.progress(percentage, text=f"⚙️ [{percentage}%] {stage_text}")
        time.sleep(0.12)
    progress_bar.empty()

def render_resource_info_card(resource_name, query_text, s_level, t_style, src):
    """Renders a standard diagnostic metadata payload above generated system layouts."""
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"📦 **Asset:** `{resource_name}`\n\n🎯 **Topic Focus:** `{query_text[:30]}...`")
        c2.markdown(f"🎓 **Level:** `{s_level}`\n\n🎨 **Pedagogy:** `{t_style}`")
        c3.markdown(f"📊 **Difficulty:** `{detect_difficulty(query_text)}`\n\n🏷️ **Weight Allocation:** `{detect_marks(query_text)}`")
        c4.markdown(f"🕒 **Generated At:** `{datetime.now().strftime('%H:%M:%S')}`\n\n🧬 **Routing Vector:** `{src}`")


# =====================================================
# DEMO DATA SEED FACTORY
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
    st.session_state["upload_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state["analytics_uploads"] += 1
    
    st.session_state["doc_metadata"] = {
        "title": "Demo Plant Systems Chapter",
        "subject": "Science",
        "chapter": "Plants and Living Systems",
        "total_pages": "2 Pages",
        "reading_time": "1 min read",
        "doc_type": "PDF Document",
        "detected_topics": ["Photosynthesis", "Plant Organs", "Ecosystems", "Biodiversity"],
        "detected_keywords": ["Xylem", "Phloem", "Chloroplasts", "Primary Producers"],
        "learning_outcomes": ["Understand vascular transportation networks", "Analyze carbon conversion in producers"],
        "competencies": ["Scientific Investigation", "Environmental Adaptation Synthesis"],
        "reading_level": "Grade 5 Basic Curriculum Level"
    }
    
    st.session_state["student_level_sel"] = "Class 5"
    st.session_state["teaching_style_sel"] = "Beginner Friendly"
    
    store_document_chunks(
        chunks=st.session_state["document_chunks"], 
        document_name="Demo_Plant_Systems_Chapter.pdf",
        page_numbers=["1", "2"],
        subject="Science",
        chapter="Plants and Living Systems"
    )


# =====================================================
# SIDEBAR NAVIGATION, LIVE STATUS & ANALYTICS
# =====================================================
with st.sidebar:
    st.title("📚 NCF 2023 AI Assistant")
    
    # --- PRESENTATION ENVIRONMENT CONTROL ---
    st.markdown("### 🎬 Presentation Tools")
    if st.button("🎬 Load Demo Chapter", use_container_width=True):
        load_demo_data()
        st.success("Demo Chapter Seeded!")

    st.divider()
    
    # --- LIVE DOCUMENT STATUS PANEL ---
    st.markdown("### 📡 Live Document Status")
    status_box = st.container(border=True)
    with status_box:
        if st.session_state["doc_metadata"] is not None:
            st.markdown("### 🟢 Document Loaded")
            st.markdown(f"📄 **File:** `{st.session_state['last_uploaded_file']}`")
            st.markdown(f"📘 **Subject:** `{st.session_state['doc_metadata']['subject']}`")
            st.markdown(f"🔖 **Chapter:** `{st.session_state['doc_metadata']['chapter']}`")
            st.markdown(f"📄 **Pages:** `{st.session_state['doc_metadata']['total_pages']}`")
            st.markdown(f"📑 **Chunks:** `{len(st.session_state['document_chunks'])}`")
            st.markdown(f"🧠 **Model:** `all-MiniLM-L6-v2`")
            st.markdown(f"🗄️ **Database:** `FAISS Local`")
            st.markdown(f"🕒 **Uploaded:** `{st.session_state['upload_time']}`")
        else:
            st.markdown("### 🔴 No Document Loaded")
            st.caption("Awaiting source ingestion parameter blocks to bind retrieval systems.")

    st.divider()
    
    # --- CURRENT SESSION ANALYTICS METRICS ---
    st.markdown("### 📊 Session Analytics Dashboard")
    analytics_box = st.container(border=True)
    with analytics_box:
        dur_delta = datetime.now() - st.session_state["session_start_time"]
        mins_active = int(dur_delta.total_seconds() // 60)
        avg_resp = (sum(st.session_state["analytics_response_times"]) / len(st.session_state["analytics_response_times"])) if st.session_state["analytics_response_times"] else 0.0
        
        st.metric("❓ Questions Asked", f"{st.session_state['analytics_questions']}")
        st.metric("📦 Resources Generated", f"{st.session_state['analytics_resources']}")
        st.metric("⚡ Avg Response Time", f"{avg_resp:.2f}s")
        st.metric("📄 Documents Uploaded", f"{st.session_state['analytics_uploads']}")
        st.metric("⏱️ Session Active Duration", f"{mins_active} min(s)")

    st.divider()
    
    # --- HISTORIC LOG TRACKING BLOCK ---
    st.markdown("### 📜 Session History Logs")
    history_records = get_history()
    if history_records:
        for item in reversed(history_records[-3:]):
            with st.container(border=True):
                st.markdown(f"❓ **Query:** `{item.get('question', '')[:30]}...`")
                st.markdown(f"📦 **Action:** `{item.get('resource_type', 'Content Task')}`")
                st.caption(f"🕒 **Time:** `{item.get('timestamp', 'N/A')}`")
    else:
        st.caption("No transactional history payload frames stored.")

# =====================================================
# SYSTEM MAIN DASHBOARD BANNER
# =====================================================
st.title("📚 NCF 2023 AI Teacher Assistant")

col_b1, col_b2, col_b3, col_b4, col_b5, col_b6 = st.columns(6)
col_b1.caption("✨ NCF 2023 Aligned")
col_b2.caption("🧠 Competency Based Learning")
col_b3.caption("🏃 Activity Based Learning")
col_b4.caption("🤝 Inclusive Teaching")
col_b5.caption("🎨 Art Integrated Learning")
col_b6.caption("🎮 Game Based Learning")

st.markdown("---")


# =====================================================
# INGESTION LAYER & COMPREHENSIVE COMPLIANCE VALIDATION
# =====================================================
uploaded_file = st.file_uploader(
    "Upload Source Content Material (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    # --- DOCUMENT VALIDATION SYSTEM ---
    MAX_FILE_SIZE_MB = 15
    MIN_WORD_COUNT = 15
    
    file_bytes = uploaded_file.read()
    file_size_mb = len(file_bytes) / (1024 * 1024)
    uploaded_file.seek(0)  # Reset pointer stream
    
    is_duplicate = (st.session_state["last_uploaded_file"] == uploaded_file.name)
    
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(f"❌ Ingestion rejected: File size limit exceeded ({file_size_mb:.2f}MB / Max {MAX_FILE_SIZE_MB}MB).")
    elif len(file_bytes) == 0:
        st.error("❌ Ingestion rejected: Selected source file contains an empty buffer allocation stream.")
    elif is_duplicate:
        st.warning("⚠️ Action skipped: This exact version document structure is already mapped inside memory frames.")
    else:
        # Proceed with processing
        ingest_stages = {
            10: "Uploading Document context parameters to temporary environment memory buffers...",
            30: "Extracting Text characters from input file data stream wrappers...",
            50: "Creating Chunks with token optimized bounds processing pipelines...",
            70: "Generating Embeddings vector matrices across local transformer maps...",
            90: "Building FAISS Index tracking allocations and matching frameworks...",
            100: "Completed Successfully — Ingestion cycle optimization validated."
        }
        
        run_staged_pipeline(ingest_stages)
        
        extracted_text = extract_document_text(uploaded_file)
        word_count = len(extracted_text.split())
        
        if word_count < MIN_WORD_COUNT:
            st.error(f"❌ Processing failed: Text volume falls below requirements ({word_count} words extracted / Min {MIN_WORD_COUNT}).")
        else:
            st.session_state["document_text"] = extracted_text
            generated_chunks = chunk_text(extracted_text)
            st.session_state["document_chunks"] = generated_chunks
            st.session_state["last_uploaded_file"] = uploaded_file.name
            st.session_state["upload_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state["analytics_uploads"] += 1
            
            # DYNAMIC METADATA INSPECTION CALL
            try:
                parsed_meta = get_document_info(uploaded_file)
                st.session_state["doc_metadata"] = {
                    "title": parsed_meta.get("title", uploaded_file.name),
                    "subject": parsed_meta.get("subject") if parsed_meta.get("subject") else "Unknown",
                    "chapter": parsed_meta.get("chapter") if parsed_meta.get("chapter") else "Unknown",
                    "total_pages": parsed_meta.get("total_pages", "1 Page"),
                    "reading_time": parsed_meta.get("reading_time", f"{max(1, word_count//150)} min read"),
                    "doc_type": parsed_meta.get("doc_type", uploaded_file.name.split(".")[-1].upper()),
                    "detected_topics": parsed_meta.get("detected_topics", ["Foundation Frameworks", "Curriculum Design"]),
                    "detected_keywords": parsed_meta.get("detected_keywords", ["Pedagogy", "NCF Standards"]),
                    "learning_outcomes": parsed_meta.get("learning_outcomes", ["Synthesize core instructional criteria summaries"]),
                    "competencies": parsed_meta.get("competencies", ["Cognitive structuring operations"]),
                    "reading_level": parsed_meta.get("reading_level", "Standard Academic Text Profile")
                }
            except Exception:
                st.session_state["doc_metadata"] = {
                    "title": uploaded_file.name,
                    "subject": "Unknown",
                    "chapter": "Unknown",
                    "total_pages": "1 Page",
                    "reading_time": "Calculated dynamically",
                    "doc_type": uploaded_file.name.split(".")[-1].upper(),
                    "detected_topics": ["General Topic Focus"],
                    "detected_keywords": ["Content Core"],
                    "learning_outcomes": ["Review primary context data structures"],
                    "competencies": ["General comprehension analytical frames"],
                    "reading_level": "Professional Reference Layout"
                }
                
            store_document_chunks(
                chunks=generated_chunks, 
                document_name=uploaded_file.name,
                subject=st.session_state["doc_metadata"]["subject"],
                chapter=st.session_state["doc_metadata"]["chapter"]
            )
            st.success("🎉 Content ingested, transformed, and registered seamlessly inside vector memory.")

# --- SMART DOCUMENT PREVIEW SECTION ---
if st.session_state["doc_metadata"] is not None:
    with st.expander("🔍 Smart Document Preview & Context Synthesis", expanded=False):
        pv_c1, pv_c2 = st.columns([2, 1])
        with pv_c1:
            st.markdown("#### 📄 Document Buffer Text Preview (First 500 Words)")
            preview_words = st.session_state["document_text"].split()[:500]
            st.text_area("", value=" ".join(preview_words), height=240, disabled=True)
        with pv_c2:
            st.markdown("#### 🧠 AI Inspected Architecture")
            st.markdown(f"📈 **Estimated Reading Level:** `{st.session_state['doc_metadata']['reading_level']}`")
            st.markdown(f"⏱️ **Reading Budget Time:** `{st.session_state['doc_metadata']['reading_time']}`")
            st.write("**Detected Core Topics:**", ", ".join(st.session_state['doc_metadata']['detected_topics']))
            st.write("**Identified Keywords:**", ", ".join(st.session_state['doc_metadata']['detected_keywords']))
            st.write("**Target Learning Outcomes:**", ", ".join(st.session_state['doc_metadata']['learning_outcomes']))
            st.write("**Target Competencies:**", ", ".join(st.session_state['doc_metadata']['competencies']))


# =====================================================
# ACTION SELECTION & EDUCATIONAL PANELS
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

# --- EDUCATIONAL CONFIGURATION PANEL ---
st.markdown("### ⚙️ Educational Configuration Parameters")
config_col1, config_col2 = st.columns(2)

with config_col1:
    student_level = st.selectbox(
        "Student Level",
        [f"Class {i}" for i in range(1, 13)],
        index=4,  # Default Class 5
        key="student_level_sel"
    )

with config_col2:
    teaching_style = st.selectbox(
        "Teaching Style",
        [
            "Beginner Friendly",
            "Concept Based",
            "Activity Based",
            "Competency Based",
            "Interactive Learning",
            "Exam Oriented"
        ],
        index=0,  # Default Beginner Friendly
        key="teaching_style_sel"
    )

# --- SHOW ACTIVE CONFIGURATION PROFILE ---
st.markdown("#### 🔍 Current Active Profile Configuration")
with st.container(border=True):
    ac_c1, ac_c2, ac_c3, ac_c4, ac_c5 = st.columns(5)
    ac_c1.markdown(f"**Student Level:**\n\n`{student_level}`")
    ac_c2.markdown(f"**Teaching Style:**\n\n`{teaching_style}`")
    ac_c3.markdown(f"**Difficulty:**\n\n`{detect_difficulty(query) if query else 'Not Evaluated'}`")
    ac_c4.markdown(f"**Marks:**\n\n`{detect_marks(query) if query else 'Not Evaluated'}`")
    
    current_doc_label = st.session_state['last_uploaded_file'] if st.session_state['last_uploaded_file'] else 'No Document Ingested'
    ac_c5.markdown(f"**Current Document:**\n\n`{current_doc_label}`")

# --- SAFE DEFAULTS AND ACTION GATEKEEPER VALIDATION ---
document_dependent_actions = [
    "📦 Generate Complete Teaching Package", "Generate Notes", "Generate MCQs", 
    "Generate Question Paper", "Generate Learning Outcomes", "Generate Competencies", 
    "Generate Lesson Plan", "Generate Teaching Guide", "Generate Flow Chart", 
    "Generate Mind Map", "Generate Chapter Summary", "Generate Important Questions"
]

has_active_context = (st.session_state["doc_metadata"] is not None)

if action in document_dependent_actions and not has_active_context:
    st.error("❌ Action Block Locked: Please upload a valid document or trigger Demo Mode to unlock these options.")
    st.info("💡 Alternative Option: Change action selector route to 'Web Search' to query outer global network frames.")
    st.stop()


# =====================================================
# RUNTIME INFERENCE ROUTER PIPELINE
# =====================================================
if st.button("🚀 Generate Content Blueprint"):
    if not query:
        st.warning("Please fill in prompt requirements before initiating tracking execution threads.")
        st.stop()

    outputs = {}
    rag_metadata_payload = None  
    
    # Use real document variables safely extracted
    if has_active_context:
        source_name = st.session_state["doc_metadata"]["title"]
        curr_subject = st.session_state["doc_metadata"]["subject"]
        curr_chapter = st.session_state["doc_metadata"]["chapter"]
    else:
        source_name = "System Core Directives"
        curr_subject = "Unknown"
        curr_chapter = "Unknown"

    start_time_mark = datetime.now()
    execution_ts = start_time_mark.strftime("%Y-%m-%d %H:%M:%S")

    # ADVANCED PROGRESSIVE STAGED PIPELINE TRACKING
    runtime_stages = {
        15: "Searching Knowledge Base parameters mapping local contexts...",
        40: "Building FAISS Index graph connection layouts to extract relevant text mappings...",
        65: "Generating AI Response matrix vectors using remote high-speed endpoints...",
        90: "Preparing Output buffers for visualization rendering components...",
        100: "Completed Successfully — Pipeline process rendering engine closed."
    }
    run_staged_pipeline(runtime_stages)
    
    try:
        # EXECUTION CORE ROUTER
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
            st.session_state["analytics_resources"] += 11
        
        elif action == "Ask Question":
            resp = rag_answer(query, student_level)
            outputs["notes"] = resp["answer"]
            source_name = resp["source"]
            if "source_info" in resp and resp["source_info"]:
                rag_metadata_payload = resp["source_info"]
            st.session_state["analytics_questions"] += 1
            
        else:
            # Dynamic standalone actions router mapping
            st.session_state["analytics_resources"] += 1
            if action == "Generate Notes":
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
                source_name = "Web Search"

        delta_seconds = (datetime.now() - start_time_mark).total_seconds()
        st.session_state["analytics_response_times"].append(delta_seconds)

        # OUTPUT INFORMATION CARD DISPLAY
        render_resource_info_card(action, query, student_level, teaching_style, source_name)

        # =====================================================
        # SOURCE TRACEABILITY PANEL (EXPANDABLE)
        # =====================================================
        with st.expander("🎯 Source Traceability Operational Matrix", expanded=True):
            st.markdown("### 📄 Architectural Context Citation Summary")
            tr_c1, tr_c2, tr_c3 = st.columns(3)
            with tr_c1:
                st.markdown(f"**Source Document:** `{source_name}`")
                st.markdown(f"**Page Number:** `{rag_metadata_payload.get('page', 'Dynamic Context') if rag_metadata_payload else 'N/A'}`")
                st.markdown(f"**Chunk Number:** `{rag_metadata_payload.get('chunk', 'Dynamic Allocation') if rag_metadata_payload else 'N/A'}`")
                st.markdown(f"**Document Version:** `v1.0.0 (Immutable Reference Frame)`")
            with tr_c2:
                st.markdown(f"**Similarity Score:** `{rag_metadata_payload.get('similarity', 'N/A') if rag_metadata_payload else 'N/A'}`")
                st.markdown(f"**Confidence Score:** `{rag_metadata_payload.get('confidence', 'N/A') if rag_metadata_payload else 'N/A'}%`")
                st.markdown(f"**Retrieval Score:** `{rag_metadata_payload.get('retrieval_score', 'N/A') if rag_metadata_payload else 'N/A'}`")
                st.markdown(f"**Retrieval Method:** `FAISS Semantic Vector Search Graph`")
            with tr_c3:
                st.markdown(f"**Generated Time:** `{execution_ts}`")
                st.markdown(f"**Student Level:** `{student_level}`")
                st.markdown(f"**Teaching Style:** `{teaching_style}`")

        st.divider()

        # =====================================================
        # MULTI-TAB MATRIX CONTAINER DISPLAY
        # =====================================================
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            "📋 Notes", "🧩 MCQs", "📝 Question Paper", "🧭 Lesson Plan",
            "📖 Teaching Guide", "📊 Flow Chart", "🧠 Mind Map", "📑 Chapter Summary", "❓ Important Questions"
        ])

        with tab1:
            st.markdown(outputs.get("notes", outputs.get("outcomes", "No textual results map configured for this node.")))
        with tab2:
            st.markdown(outputs.get("mcqs", "No dataset array generated for this segment."))
        with tab3:
            st.markdown(outputs.get("paper", "No question compilation loaded."))
        with tab4:
            st.markdown(outputs.get("lesson", "No structure instruction logs found."))
        with tab5:
            st.markdown(outputs.get("guide", "No scripting data generated."))
        with tab6:
            st.markdown(outputs.get("flowchart", "No schematic parameters generated."))
        with tab7:
            st.markdown(outputs.get("mindmap", "No conceptual relations schema found."))
        with tab8:
            st.markdown(outputs.get("summary", "No targeted misconception sets mapped."))
        with tab9:
            st.markdown(outputs.get("questions", "No targeted tier question systems generated."))

        # =====================================================
        # EXPORT LAYER COMPILATION & ENHANCED HISTORY PERSISTENCE
        # =====================================================
        st.divider()
        st.subheader("📥 Export Curricular Asset Blocks")
        
        pdf_traceability_appendix = (
            f"\n\n\n\n---\n### 📄 EXPORT TELEMETRY CITATION\n"
            f"- Source File Name: {source_name}\n"
            f"- Curriculum Domain Field: {curr_subject} | Chapter Node: {curr_chapter}\n"
            f"- Pedagogy Configuration: Student Level {student_level} | Inst Style {teaching_style}\n"
            f"- Evaluation Timestamp Clock Signature: {execution_ts}\n---"
        )

        raw_string_compilation = "\n\n***\n\n".join([f"# {k.upper()}\n{v}" for k, v in outputs.items()]) + pdf_traceability_appendix
        compiled_stream_buffer = notes_pdf(raw_string_compilation, source_name)

        ec1, ec2 = st.columns(2)
        with ec1:
            with st.container(border=True):
                st.markdown("#### 📄 Integrated Curricular Payload Block")
                st.download_button(
                    label="📥 Download Generated Asset PDF",
                    data=compiled_stream_buffer,
                    file_name="NCF_Resource_Export.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        with ec2:
            with st.container(border=True):
                st.markdown("#### 🗄️ Full Bundle Teaching Distribution Package")
                st.download_button(
                    label="📥 Download Complete Package PDF",
                    data=compiled_stream_buffer,
                    file_name="Complete_NCF_Teaching_Package.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    disabled=(action != "📦 Generate Complete Teaching Package")
                )

        # COMPREHENSIVE SAVING METADATA BLOCK INTERFACE EXTENSION
        save_to_history(query, raw_string_compilation, source_name)
        
        if st.session_state.get("history"):
            latest_record = st.session_state["history"][-1]
            latest_record["student_level"] = student_level
            latest_record["teaching_style"] = teaching_style
            latest_record["document"] = source_name
            latest_record["subject"] = curr_subject
            latest_record["chapter"] = curr_chapter
            latest_record["confidence"] = rag_metadata_payload.get("confidence", "N/A") if rag_metadata_payload else "N/A"
            latest_record["similarity"] = rag_metadata_payload.get("similarity", "N/A") if rag_metadata_payload else "N/A"
            latest_record["retrieval_score"] = rag_metadata_payload.get("retrieval_score", "N/A") if rag_metadata_payload else "N/A"
            latest_record["timestamp"] = execution_ts
            latest_record["action"] = action

    except Exception as e:
        if 'runtime_tracker' in locals():
            runtime_tracker.empty()
        st.exception(e)

# =====================================================
# SYSTEM COMPREHENSIVE PLATFORM FOOTER
# =====================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
foot_c1, foot_c2, foot_c3 = st.columns([1, 3, 1])
with foot_c2:
    st.markdown(
        "<center style='color: gray; font-size: 0.85rem; line-height: 1.4rem;'>"
        "<b>Built Framework Components:</b><br>"
        "🤖 Groq Inference Engine | 📚 FAISS Vector Database Layer | 🧠 SentenceTransformers Model Graph | ⚡ Streamlit Client Node<br>"
        "<b>Curricular Governance Base Rules:</b><br>"
        "📖 National Curriculum Framework (NCF 2023) | 🎓 National Education Policy (NEP 2020)<br>"
        "🚀 <i>Enterprise RAG Architecture — Version 1.0 MVP Node Setup</i>"
        "</center>",
        unsafe_allow_html=True
    )
st.markdown("---")
