import streamlit as st
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Teacher Assistant",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("📚 AI Teacher Assistant")

    st.markdown("### History")

    if len(st.session_state.history) == 0:
        st.info("No history yet.")
    else:
        for item in reversed(st.session_state.history[-10:]):
            st.write(f"• {item}")

    st.divider()

    st.markdown("### What can AI do?")

    st.markdown("""
    ✅ Explain Topics

    ✅ Generate Notes

    ✅ Generate MCQs

    ✅ Generate Question Papers

    ✅ Generate Lesson Plans

    ✅ Generate Teaching Guides

    ✅ Generate Homework

    ✅ Generate Worksheets

    ✅ Download PDF

    """)

# -----------------------------
# HEADER
# -----------------------------
st.title("📚 AI Teacher Assistant")

st.markdown("""
Upload a document and ask anything.

**Default Mode:** Explain like a Class 5 Student.
""")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Document",
    type=["pdf", "docx", "pptx", "png", "jpg", "jpeg"]
)

# -----------------------------
# SETTINGS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    student_level = st.selectbox(
        "Student Level",
        [
            "Class 5 (Default)",
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

# -----------------------------
# QUICK ACTIONS
# -----------------------------
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

# -----------------------------
# USER QUERY
# -----------------------------
query = st.text_area(
    "Ask Anything",
    placeholder="""
Examples:

Explain Photosynthesis

Generate Notes

Generate Easy MCQs

Generate Hard Question Paper

How should I teach this chapter?
"""
)

# -----------------------------
# PROCESS
# -----------------------------
if st.button("🚀 Generate"):

    if query.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    st.session_state.history.append(query)

    with st.spinner("AI is thinking..."):

        response = f"""
### Sample Response

You asked:

**{query}**

Student Level:
**{student_level}**

Teaching Style:
**{teaching_style}**

This is where OpenRouter response will appear.

By default all explanations should be generated
like a Class 5 student can understand.

Example:

Plants make their own food using sunlight.
This process is called photosynthesis.

Think of a plant like a tiny kitchen.
"""

        st.success("Generated Successfully")

        st.markdown(response)

        st.divider()

        st.subheader("📌 Source")

        st.success("✓ Uploaded Document")

        st.divider()

        st.download_button(
            label="📄 Download PDF",
            data=response,
            file_name="teacher_assistant_output.txt",
            mime="text/plain"
        )

# -----------------------------
# QUICK ACTION RESULTS
# -----------------------------
if explain_btn:
    st.info("Explain Topic selected")

if notes_btn:
    st.info("Generate Notes selected")

if mcq_btn:
    st.info("Generate MCQs selected")

if qp_btn:
    st.info("Generate Question Paper selected")

if lesson_btn:
    st.info("Generate Lesson Plan selected")

if guide_btn:
    st.info("Generate Teaching Guide selected")

# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    f"AI Teacher Assistant • {datetime.now().strftime('%Y-%m-%d')}"
)
