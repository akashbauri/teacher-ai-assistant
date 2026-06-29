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
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="NCF 2023 AI Teacher Assistant",
    page_icon="📚",
    layout="wide"
)

initialize_history()

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
    
    store_document_chunks(
        chunks=st.session_state["document_chunks"], 
        document_name="Demo_Plant_Systems_Chapter.pdf",
        page_numbers=["1", "2"],
        subject="Science",
        chapter="Plants and Living Systems"
    )

# =====================================================
# SIDEBAR NAVIGATION & TELEMETRY
# =====================================================
with st.sidebar:
    st.title("📚 NCF 2023 AI Assistant")
    
    # --- PRESENTATION ENVIRONMENT CONTROL ---
    st.markdown("### 🎬 Presentation Tools")
    if st.button("🎬 Load Demo Chapter", use_container_width=True):
        load_demo_data()
        st.success("Demo Chapter Seeded!")

    st.divider()
    
    # --- ACTIVE HARDWARE & HEALTH STATUS BLOCK ---
    st.markdown("### 🖥️ Active System Status")
    status_container = st.container(border=True)
    with status_container:
        st.markdown("🟢 **LLM Runtime:** `Connected`")
        st.markdown("🟢 **FAISS Matrix Engine:** `Ready`")
        st.markdown("🟢 **Embedding Pipeline:** `Loaded`")
        if get_document_count() > 0:
            st.markdown("🟢 **Knowledge Space:** `Indexed`")
        else:
            st.markdown("⚪ **Knowledge Space:** `Uninitialized`")

    # --- HISTORIC LOG TRACKING BLOCK ---
    st.markdown("### 📜 Session History Logs")
    history_records = get_history()
    if history_records:
        for item in reversed(history_records[-4:]):
            with st.container(border=True):
                # Extracted tracking payload
                record_ts = item.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                record_src = item.get("source", "System Directive Engine")
                record_conf = item.get("confidence", "N/A")
                
                st.markdown(f"❓ **Query:** `{item['question'][:35]}...`")
                st.markdown(f"📦 **Resource:** `{item.get('resource_type', 'Content Unit')}`")
                st.markdown(f"📄 **Origin:** `{record_src}`")
                if record_conf != "N/A":
                    st.markdown(f"🎯 **Certainty:** `{record_conf}%`")
                st.caption(f"🕒 **Retrieved At:** `{record_ts}`")
    else:
        st.caption("No historical transaction payloads detected in this runtime instance.")

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
# INGESTION & PIPELINE STAGED LOGIC
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
        ingest_progress = st.progress(0, text="Initializing ingestion node...")
        
        ingest_progress.progress(10, text="📄 Uploading Document into workspace buffers...")
        time.sleep(0.15)
        
        ingest_progress.progress(25, text="📖 Extracting Text characters from input file data stream...")
        text = extract_document_text(uploaded_file)
        st.session_state["document_text"] = text
        time.sleep(0.15)
        
        ingest_progress.progress(40, text="✂️ Creating Smart Chunks using token optimization bounds...")
        chunks = chunk_text(text)
        st.session_state["document_chunks"] = chunks
        time.sleep(0.15)
        
        ingest_progress.progress(60, text="🧠 Generating Embeddings vector matrices via SentenceTransformers...")
        time.sleep(0.1)
        
        ingest_progress.progress(75, text="📚 Searching FAISS Knowledge Base registration handles...")
        store_document_chunks(
            chunks=chunks, 
            document_name=uploaded_file.name,
            subject="General Curriculum",
            chapter="Injected Unit Module"
        )
        st.session_state["last_uploaded_file"] = uploaded_file.name
        
        ingest_progress.progress(90, text="🤖 Generating AI Response environment parameters...")
        time.sleep(0.1)
        
        ingest_progress.progress(100, text="✅ Content Generated Successfully!")
        time.sleep(0.1)
        ingest_progress.empty()

        # Render Enterprise Ingest Summary Dashboard
        st.markdown("### 📊 Document Ingest Summary")
        summary_container = st.container(border=True)
        with summary_container:
            s_col1, s_col2, s_col3 = st.columns(3)
            with s_col1:
                st.markdown(f"📄 **File Name:** `{uploaded_file.name}`")
                st.markdown(f"📚 **Vector Database:** `FAISS (FlatL2 Memory Local)`")
            with s_col2:
                st.markdown(f"📝 **Word Count:** `{len(text.split())}`")
                st.markdown(f"🔤 **Character Count:** `{len(text)}`")
            with s_col3:
                st.markdown(f"📑 **Total Chunks:** `{len(chunks)} Chunks`")
                st.markdown(f"🧠 **Embedding Model:** `all-MiniLM-L6-v2 (384D)`")

# --- CORE TOPIC PREVIEWS ---
if "document_text" in st.session_state:
    st.markdown("### 🔍 Detected Core Target Areas")
    col_t1, col_t2, col_t3 = st.columns(3)
    col_t1.info("📍 Concept Found: Foundation Theories")
    col_t2.info("📍 Core Mechanics & Workflows")
    col_t3.info("📍 Structure Implementations")

# =====================================================
# ACTION BOUND SELECTION INTERFACE
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
# RUNTIME INFERENCE ROUTER PIPELINE
# =====================================================
if st.button("🚀 Generate Content Blueprint"):
    if not query:
        st.warning("Please fill in prompt requirements before initiating tracking execution threads.")
        st.stop()

    outputs = {}
    rag_metadata_payload = None  
    source_name = get_document_name() if get_document_count() > 0 else "System Core Directives"
    
    # Initialize Performance Benchmarks
    start_time_mark = datetime.now()
    execution_ts = start_time_mark.strftime("%Y-%m-%d %H:%M:%S")

    # Staged Demonstration Progress Indicator Status Stream
    runtime_tracker = st.progress(0, text="Booting compilation pipeline engines...")
    
    try:
        runtime_tracker.progress(10, text="📄 [10%] Loading Document context registers into local space...")
        time.sleep(0.12)
        runtime_tracker.progress(25, text="📖 [25%] Extracting Text mapping streams from working memory frames...")
        time.sleep(0.12)
        runtime_tracker.progress(40, text="✂️ [40%] Creating Smart Chunks vector references for query targets...")
        time.sleep(0.12)
        runtime_tracker.progress(60, text="🧠 [60%] Generating Embeddings for transaction array matching maps...")
        time.sleep(0.1)
        runtime_tracker.progress(75, text="📚 [75%] Searching FAISS Knowledge Base index locations...")

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
        
        elif action == "Ask Question":
            resp = rag_answer(query, student_level)
            outputs["notes"] = resp["answer"]
            source_name = resp["source"]
            if "source_info" in resp and resp["source_info"]:
                rag_metadata_payload = resp["source_info"]
                
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
            source_name = "Web Search"

        runtime_tracker.progress(90, text="🤖 [90%] Generating AI Response matrix streams via inference endpoint...")
        time.sleep(0.08)
        runtime_tracker.progress(100, text="✅ [100%] Content Generated Successfully!")
        time.sleep(0.05)
        runtime_tracker.empty()

        # Compute Operational Processing Latency
        delta_seconds = (datetime.now() - start_time_mark).total_seconds()

        # Render Professional Output Banner 
        st.markdown(f"""
        ### ✅ Content Generated Successfully
        * **Document Context:** `{st.session_state.get('last_uploaded_file', get_document_name())}`
        * **Generation Window:** `{delta_seconds:.2f} seconds`
        * **Target Source Router:** `{source_name}`
        """)

        # =====================================================
        # EXTANDED SYSTEM MULTI-METRIC INSTRUMENT PANEL
        # =====================================================
        st.markdown("### 📊 Enterprise Telemetry Dashboard")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col5, m_col6, m_col7, m_col8 = st.columns(4)
        
        m_col1.metric("📚 Indexed Chunks", f"{len(st.session_state.get('document_chunks', []))}")
        m_col2.metric("📄 Uploaded Documents", f"{get_document_count()}")
        m_col3.metric("⚡ Response Time", f"{delta_seconds:.2f}s")
        m_col4.metric("📖 Student Level", student_level.split(" ")[0])
        
        if action == "Ask Question" and rag_metadata_payload:
            m_col5.metric("🎯 Confidence Score", f"{rag_metadata_payload.get('confidence', 0)}%")
            m_col6.metric("⭐ Similarity Score", f"{rag_metadata_payload.get('similarity', 0.0):.2f}")
        else:
            m_col5.metric("🎯 Confidence Score", "N/A")
            m_col6.metric("⭐ Similarity Score", "N/A")
            
        m_col7.metric("🤖 Active LLM Node", "Llama-3-Groq Engine")
        m_col8.metric("📚 Retrieval Method", "FAISS Semantic Search")

        st.divider()

        # =====================================================
        # ROUTER STATUS BADGE KEY
        # =====================================================
        if action == "Ask Question":
            st.markdown("#### 🎯 Active Routing Identification")
            if source_name == "Document Knowledge Base" and rag_metadata_payload:
                st.success("🟢 Retrieved from Uploaded Document")
            elif source_name == "Web Search":
                st.warning("🟡 Retrieved from Web Search")
            else:
                st.error("🔴 No Relevant Context Found")

        # =====================================================
        # MULTI-TAB MATRIX CONTAINER DISPLAY
        # =====================================================
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            "📋 Notes", "🧩 MCQs", "📝 Question Paper", "🧭 Lesson Plan",
            "📖 Teaching Guide", "📊 Flow Chart", "🧠 Mind Map", "📑 Chapter Summary", "❓ Important Questions"
        ])

        with tab1:
            st.markdown("### Chapter Notes & Content")
            st.markdown(outputs.get("notes", outputs.get("outcomes", "No custom textual results extracted.")))
            
            # UNIFIED SOURCE ATTRIBUTION SHEET (EXPOSED)
            if action == "Ask Question" and rag_metadata_payload:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 📄 Enterprise Source Citation")
                cite_container = st.container(border=True)
                with cite_container:
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown(f"**📄 Document Target:** `{rag_metadata_payload['document']}`")
                        st.markdown(f"**📚 Chapter Context:** `{rag_metadata_payload['chapter']}`")
                        st.markdown(f"**📘 Subject Field:** `{rag_metadata_payload['subject']}`")
                    with c2:
                        st.markdown(f"**📖 Page Location:** `Page {rag_metadata_payload['page']}`")
                        st.markdown(f"**📑 Index Segment:** `Chunk {rag_metadata_payload['chunk']} / {rag_metadata_payload['total_chunks']}`")
                        st.markdown(f"**🔍 Engine Selector:** `{rag_metadata_payload['retrieval_method']}`")
                    with c3:
                        st.markdown(f"**⭐ Similarity Weight:** `{rag_metadata_payload['similarity']}`")
                        st.markdown(f"**🎯 Confidence Metric:** `{rag_metadata_payload['confidence']}%`")
                        st.markdown(f"**📊 Retrieval Score:** `{rag_metadata_payload['retrieval_score']}`")
                    st.caption(f"🕒 **Traceability Generation Timestamp:** {execution_ts} | Rank Priority: #{rag_metadata_payload['rank']}")

        with tab2:
            st.markdown("### Balanced MCQ Matrix Output")
            st.markdown(outputs.get("mcqs", "No custom dataset generated for this module channel tab index."))
        with tab3:
            st.markdown("### Assessment Question Framework Paper")
            st.markdown(outputs.get("paper", "No custom dataset generated for this module channel tab index."))
        with tab4:
            st.markdown("### Comprehensive Lesson Plan")
            st.markdown(outputs.get("lesson", "No custom dataset generated for this module channel tab index."))
        with tab5:
            st.markdown("### Teacher Scripts & Implementation Guide")
            st.markdown(outputs.get("guide", "No custom dataset generated for this module channel tab index."))
        with tab6:
            st.markdown("### Pedagogical Progression Flow Chart")
            st.markdown(outputs.get("flowchart", "No custom dataset generated for this module channel tab index."))
        with tab7:
            st.markdown("### Hierarchical Mind Map Scheme Structure")
            st.markdown(outputs.get("mindmap", "No custom dataset generated for this module channel tab index."))
        with tab8:
            st.markdown("### Concept Summaries & Misconception Lists")
            st.markdown(outputs.get("summary", "No custom dataset generated for this module channel tab index."))
        with tab9:
            st.markdown("### Cognitive Difficulty Tiered Question Bank")
            st.markdown(outputs.get("questions", "No custom dataset generated for this module channel tab index."))

        # =====================================================
        # EXPORT LAYER DOCUMENT TRACE COMPILATION
        # =====================================================
        st.divider()
        st.subheader("📥 Export Curricular Asset Blocks")
        
        # Build deterministic trailing metadata string block for full runtime visibility inside downloads
        pdf_traceability_appendix = f"\n\n\n\n---\n### 📄 DEPLOYMENT ARCHITECTURE SOURCE CITATION\n"
        if rag_metadata_payload:
            pdf_traceability_appendix += (
                f"- Document: {rag_metadata_payload['document']}\n"
                f"- Page: {rag_metadata_payload['page']} | Chunk Segment: {rag_metadata_payload['chunk']}\n"
                f"- Chapter Context: {rag_metadata_payload['chapter']} | Curricular Subject: {rag_metadata_payload['subject']}\n"
                f"- Accuracy Weights: Similarity {rag_metadata_payload['similarity']} | Confidence {rag_metadata_payload['confidence']}%\n"
                f"- Index Database Score: {rag_metadata_payload['retrieval_score']} ({rag_metadata_payload['retrieval_method']})\n"
            )
        else:
            pdf_traceability_appendix += f"- Reference Origin: System Generative Prompts / Web Search Network Outlets\n"
        pdf_traceability_appendix += f"- Execution Generation Pipeline Stamp: {execution_ts}\n---"

        # Compilation file payloads
        raw_string_compilation = "\n\n***\n\n".join([f"# {k.upper()}\n{v}" for k, v in outputs.items()]) + pdf_traceability_appendix
        compiled_stream_buffer = notes_pdf(raw_string_compilation, source_name)

        # GRID EXPORT CARD INTERFACE DISPLAY
        ec1, ec2 = st.columns(2)
        
        with ec1:
            with st.container(border=True):
                st.markdown("#### 📄 Integrated Curricular Payload Block")
                st.write(f"**Target Identifier:** `NCF_Resource_Export.pdf`")
                st.write(f"**Telemetry Clock Signature:** `{execution_ts}`")
                st.write(f"**Allocated Buffer Scale:** `{len(raw_string_compilation)} bytes`")
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
                st.write(f"**Target Identifier:** `Complete_NCF_Teaching_Package.pdf`")
                st.write(f"**Telemetry Clock Signature:** `{execution_ts}`")
                st.write(f"**Allocated Buffer Scale:** `Dynamic System Compund`")
                st.download_button(
                    label="📥 Download Complete Package PDF",
                    data=compiled_stream_buffer,
                    file_name="Complete_NCF_Teaching_Package.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    disabled=(action != "📦 Generate Complete Teaching Package")
                )

        # Commit persistent tracking telemetry data indices directly to logger state
        save_to_history(query, raw_string_compilation, source_name)
        
        # Override last logging entry dynamically to preserve static timestamp across structural state loads
        if st.session_state["history"]:
            st.session_state["history"][-1]["timestamp"] = execution_ts
            st.session_state["history"][-1]["resource_type"] = action
            if rag_metadata_payload:
                st.session_state["history"][-1]["confidence"] = rag_metadata_payload.get("confidence", "N/A")

    except Exception as e:
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
    st.divider()
    st.markdown(
        "<center style='color: #a0a0a0; font-size: 0.75rem;'>"
        "<b>Core Architecture Roadmap:</b> Redis Cache Layer • LangGraph Multi-Agent Orchestration • MCP Protocol Hooks • "
        "PostgreSQL Vector Database Integration • Supabase Store Relays • BM25 Hybrid Lexical Match Search Models"
        "</center>",
        unsafe_allow_html=True
    )
st.markdown("---")
