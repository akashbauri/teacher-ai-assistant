import streamlit as st
from tavily import TavilyClient

# ==========================================
# HISTORY MANAGEMENT
# ==========================================

def initialize_history():
    """
    Initialize session history.
    """

    if "history" not in st.session_state:
        st.session_state.history = []


def save_to_history(
    question,
    answer,
    source
):
    """
    Save interaction.
    """

    st.session_state.history.append(
        {
            "question": question,
            "answer": answer,
            "source": source
        }
    )


def get_history():
    """
    Return chat history.
    """

    return st.session_state.history


# ==========================================
# SOURCE TRACKING
# ==========================================

def build_source_label(
    document_used=False,
    web_used=False
):
    """
    Return source label.
    """

    if document_used and web_used:
        return "✓ Uploaded Document + ✓ Web Search"

    if document_used:
        return "✓ Uploaded Document"

    if web_used:
        return "✓ Web Search"

    return "Unknown Source"


# ==========================================
# TAVILY SEARCH
# ==========================================

def search_web(
    query,
    max_results=5
):
    """
    Search using Tavily.
    """

    try:

        client = TavilyClient(
            api_key=st.secrets["TAVILY_API_KEY"]
        )

        results = client.search(
            query=query,
            max_results=max_results
        )

        return results

    except Exception as e:

        return {
            "error": str(e)
        }


# ==========================================
# FORMAT WEB RESULTS
# ==========================================

def format_web_results(results):
    """
    Convert Tavily output to text.
    """

    if not results:
        return ""

    if "results" not in results:
        return ""

    output = []

    for item in results["results"]:

        title = item.get("title", "")
        content = item.get("content", "")

        output.append(
            f"Title: {title}\nContent: {content}"
        )

    return "\n\n".join(output)


# ==========================================
# DOCUMENT PLACEHOLDER
# ==========================================

def extract_document_text(uploaded_file):
    """
    MVP placeholder.

    Later:
    PDF
    DOCX
    PPTX
    OCR
    ChromaDB

    will be added here.
    """

    if uploaded_file is None:
        return ""

    return f"""
    Uploaded File:
    {uploaded_file.name}

    Document extraction module
    will be connected in Phase 2.
    """


# ==========================================
# QUICK ACTION DETECTION
# ==========================================

def detect_action(user_query):

    text = user_query.lower()

    if "mcq" in text:
        return "mcqs"

    if "question paper" in text:
        return "question paper"

    if "lesson plan" in text:
        return "lesson plan"

    if "teaching guide" in text:
        return "teaching guide"

    if "notes" in text:
        return "notes"

    if "homework" in text:
        return "homework"

    if "worksheet" in text:
        return "worksheet"

    return "explain"


# ==========================================
# LEVEL NORMALIZATION
# ==========================================

def normalize_level(level):

    if "Class 5" in level:
        return "Class 5"

    return level


# ==========================================
# MARKS PARSER
# ==========================================

def detect_marks(text):

    text = text.lower()

    if "20 mark" in text:
        return 20

    if "30 mark" in text:
        return 30

    if "50 mark" in text:
        return 50

    return 20


# ==========================================
# DIFFICULTY PARSER
# ==========================================

def detect_difficulty(text):

    text = text.lower()

    if "easy" in text:
        return "Easy"

    if "moderate" in text:
        return "Moderate"

    if "hard" in text:
        return "Hard"

    return "Mixed"
